from __future__ import annotations

from typing import Any
from urllib.parse import quote

import httpx

from app.core.config import settings


def _normalize_base_url(raw: str) -> str:
    base = raw.rstrip("/")
    if "api.foursquare.com/v3" in base:
        return "https://places-api.foursquare.com"
    if base.endswith("/places"):
        base = base.removesuffix("/places")
    return base


class FoursquarePlacesService:
    """Foursquare Places API (yeni endpoint) — otel arama, ipuçları ve fotoğraflar."""

    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key or settings.foursquare_api_key
        configured = settings.foursquare_base_url or settings.foursquare_api_base_url
        self._base_url = _normalize_base_url(configured)
        self._api_version = settings.foursquare_api_version

    def is_configured(self) -> bool:
        return bool(self._api_key)

    def _headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self._api_key or ''}",
            "X-Places-Api-Version": self._api_version,
        }

    @staticmethod
    def _category_icon_url(categories: list[dict[str, Any]] | None) -> str | None:
        if not categories:
            return None
        icon = categories[0].get("icon")
        if not isinstance(icon, dict):
            return None
        prefix = icon.get("prefix")
        suffix = icon.get("suffix")
        if isinstance(prefix, str) and isinstance(suffix, str):
            return f"{prefix}120{suffix}"
        return None

    @staticmethod
    def _maps_search_url(name: str, address: str) -> str:
        query = quote(f"{name} {address}".strip())
        return f"https://www.google.com/maps/search/?api=1&query={query}"

    async def search_hotels(self, *, city: str, limit: int = 5) -> list[dict[str, Any]]:
        if not self._api_key:
            return []

        url = f"{self._base_url}/places/search"
        params: dict[str, str | int] = {
            "query": "hotel",
            "near": f"{city}, Turkey",
            "limit": max(1, min(limit, 10)),
        }

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url, headers=self._headers(), params=params)
            response.raise_for_status()
            data = response.json()

        results = data.get("results")
        if not isinstance(results, list):
            return []

        normalized: list[dict[str, Any]] = []
        for item in results:
            if not isinstance(item, dict):
                continue

            fsq_id = str(item.get("fsq_place_id") or item.get("fsq_id") or "").strip()
            if not fsq_id:
                continue

            location = item.get("location")
            address = ""
            if isinstance(location, dict):
                address = str(location.get("formatted_address") or location.get("address") or "")

            name = str(item.get("name") or "İsimsiz Otel")
            categories = item.get("categories") if isinstance(item.get("categories"), list) else []
            category_icon = self._category_icon_url(categories)

            rating_raw = item.get("rating")
            rating = float(rating_raw) if isinstance(rating_raw, (int, float)) else None

            stats = item.get("stats")
            rating_count: int | None = None
            if isinstance(stats, dict):
                total = stats.get("total_ratings")
                if isinstance(total, int):
                    rating_count = total

            # placemaker_url bazı hesaplarda "join" sayfasına düşebildiği için
            # rezervasyon aksiyonunda daima doğrudan harita arama URL'i kullanıyoruz.
            booking_url = self._maps_search_url(name, address)

            normalized.append(
                {
                    "fsq_id": fsq_id,
                    "name": name,
                    "address": address,
                    "rating": rating,
                    "user_rating_count": rating_count,
                    "description": str(item.get("description") or ""),
                    "category_icon_url": category_icon,
                    "booking_url": booking_url,
                }
            )
        return normalized

    async def get_place_photos(self, *, fsq_id: str, limit: int = 2) -> list[str]:
        if not self._api_key or not fsq_id:
            return []

        url = f"{self._base_url}/places/{fsq_id}/photos"
        params = {"limit": max(1, min(limit, 8))}

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url, headers=self._headers(), params=params)
            if response.status_code in {401, 402, 403, 429}:
                return []
            response.raise_for_status()
            data = response.json()

        raw = data.get("results") if isinstance(data.get("results"), list) else data
        if not isinstance(raw, list):
            return []

        urls: list[str] = []
        for item in raw:
            if not isinstance(item, dict):
                continue
            prefix = item.get("prefix")
            suffix = item.get("suffix")
            if isinstance(prefix, str) and isinstance(suffix, str):
                urls.append(f"{prefix}original{suffix}")
        return urls

    async def get_place_tips(self, *, fsq_id: str, limit: int = 12) -> list[str]:
        if not self._api_key or not fsq_id:
            return []

        url = f"{self._base_url}/places/{fsq_id}/tips"
        params = {"limit": max(1, min(limit, 20))}

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url, headers=self._headers(), params=params)
            if response.status_code in {401, 402, 403, 429}:
                return []
            response.raise_for_status()
            data = response.json()

        raw = data.get("results") if isinstance(data.get("results"), list) else data
        if not isinstance(raw, list):
            return []

        texts: list[str] = []
        for tip in raw:
            if not isinstance(tip, dict):
                continue
            text = tip.get("text")
            if isinstance(text, str) and text.strip():
                texts.append(text.strip())
        return texts

    async def collect_review_texts(self, *, place: dict[str, Any]) -> list[str]:
        fsq_id = str(place.get("fsq_id") or "")
        tips = await self.get_place_tips(fsq_id=fsq_id)
        if tips:
            return tips

        fallback_parts: list[str] = []
        description = str(place.get("description") or "").strip()
        if description:
            fallback_parts.append(description)

        name = str(place.get("name") or "Otel")
        address = str(place.get("address") or "")
        if address:
            fallback_parts.append(f"Adres: {address}")

        rating = place.get("rating")
        if isinstance(rating, (int, float)):
            fallback_parts.append(f"{name} için Foursquare ortalama puanı {rating}/10.")

        count = place.get("user_rating_count")
        if isinstance(count, int):
            fallback_parts.append(f"Toplam {count} kullanıcı değerlendirmesi mevcut.")

        if fallback_parts:
            return fallback_parts

        return [f"{name} için Foursquare üzerinde henüz yeterli kullanıcı yorumu bulunamadı."]
