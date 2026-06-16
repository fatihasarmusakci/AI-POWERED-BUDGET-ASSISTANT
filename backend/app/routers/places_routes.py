from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.schemas.api import PlaceHotelAnalysis, PlaceHotelItem, PlaceHotelListResponse
from app.services.foursquare_places_service import FoursquarePlacesService
from app.services.hotel_analysis_service import HotelAnalysisService

router = APIRouter(prefix="/places", tags=["places"])


def _parse_preferences(raw: str | None) -> dict[str, Any] | None:
    if not raw:
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="preferences geçerli JSON olmalıdır.") from exc
    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="preferences bir JSON nesnesi olmalıdır.")
    return data


@router.get("/hotels", response_model=PlaceHotelListResponse)
async def get_hotels_from_places(
    city: str = Query(..., min_length=2, description="Türkiye'deki il adı"),
    limit: int = Query(default=5, ge=1, le=10),
    light: bool = Query(
        default=True,
        description="True ise fotoğraf/ipucu API çağrıları atlanır (kredi tasarrufu).",
    ),
    preferences: str | None = Query(
        default=None,
        description="Opsiyonel kullanıcı tercihleri (JSON string).",
    ),
) -> PlaceHotelListResponse:
    places_service = FoursquarePlacesService()
    if not places_service.is_configured():
        raise HTTPException(
            status_code=400,
            detail="FOURSQUARE_API_KEY ayarlanmadı. Backend .env dosyasına anahtar ekleyin.",
        )

    pref_data = _parse_preferences(preferences)
    analysis_service = HotelAnalysisService()
    try:
        places = await places_service.search_hotels(city=city, limit=limit)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"Foursquare sorgusu başarısız: {exc}") from exc

    if not places:
        raise HTTPException(status_code=404, detail=f"{city} için otel bulunamadı.")

    items: list[PlaceHotelItem] = []
    for place in places:
        fsq_id = str(place.get("fsq_id") or "")
        name = str(place.get("name") or "İsimsiz Otel")
        address = str(place.get("address") or "")
        rating_raw = place.get("rating")
        rating = float(rating_raw) if isinstance(rating_raw, (int, float)) else None
        user_rating_count_raw = place.get("user_rating_count")
        user_rating_count = int(user_rating_count_raw) if isinstance(user_rating_count_raw, int) else None

        if light:
            reviews = []
            if address:
                reviews.append(f"{name} — {address}")
            description = str(place.get("description") or "").strip()
            if description:
                reviews.append(description)
            if rating is not None:
                reviews.append(f"Foursquare ortalama puanı: {rating}/10")
            if user_rating_count is not None:
                reviews.append(f"Toplam {user_rating_count} kullanıcı değerlendirmesi")
            if not reviews:
                reviews = [f"{name} için temel otel bilgisi (hafif mod)."]
            official_photo = None
            user_photo = None
        else:
            try:
                reviews = await places_service.collect_review_texts(place=place)
            except Exception:
                reviews = [f"{name} için Foursquare verisi alınamadı."]

            photo_urls: list[str] = []
            try:
                photo_urls = await places_service.get_place_photos(fsq_id=fsq_id, limit=2)
            except Exception:
                photo_urls = []

            category_icon = place.get("category_icon_url")
            fallback_icon = str(category_icon) if isinstance(category_icon, str) else None
            official_photo = photo_urls[0] if photo_urls else fallback_icon
            user_photo = photo_urls[1] if len(photo_urls) > 1 else official_photo

        booking_url = str(place.get("booking_url") or "")

        analysis_raw = analysis_service.analyze_reviews(reviews, pref_data)
        analysis = PlaceHotelAnalysis.model_validate(analysis_raw)
        items.append(
            PlaceHotelItem(
                place_id=fsq_id,
                name=name,
                address=address,
                rating=rating,
                user_rating_count=user_rating_count,
                official_photo_url=official_photo,
                user_photo_url=user_photo,
                booking_url=booking_url or None,
                reviews=reviews,
                analysis=analysis,
            )
        )

    return PlaceHotelListResponse(city=city, items=items)
