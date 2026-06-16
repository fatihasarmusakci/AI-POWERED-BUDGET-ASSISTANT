from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class HotelAnalysisRequest(BaseModel):
    """Otel yorum analizi request modeli."""

    reviews: list[str] = Field(
        ...,
        min_length=1,
        description="Analiz edilecek otel yorumları listesi",
    )
    preferences: dict[str, Any] | None = Field(
        default=None,
        description="Kullanıcı seçimleri (travel_style, priority, non_negotiable, persona).",
    )


class HotelAnalysisResponse(BaseModel):
    """Otel yorum analizi response modeli."""

    cleaning_score: int = Field(
        ...,
        ge=1,
        le=5,
        description="Temizlik skoru (1-5 arası)",
    )
    has_playground: bool = Field(
        ...,
        description="Otelde çocuk parkı/oyun alanı var mı?",
    )
    quietness_score: int = Field(
        ...,
        ge=1,
        le=5,
        description="Sessizlik skoru (1-5 arası)",
    )

    service_score: int = Field(..., ge=1, le=5, description="Personel/servis kalitesi (1-5)")
    location_score: int = Field(..., ge=1, le=5, description="Konum avantajı (1-5)")
    wifi_score: int = Field(..., ge=1, le=5, description="Wi-Fi kalitesi/güvenilirliği (1-5)")
    breakfast_score: int = Field(..., ge=1, le=5, description="Kahvaltı kalitesi (1-5)")
    family_friendly_score: int = Field(..., ge=1, le=5, description="Aile/çocuk dostu uygunluk (1-5)")
    entertainment_score: int = Field(..., ge=1, le=5, description="Eğlence/aktivite imkanları (1-5)")
    room_comfort_score: int = Field(..., ge=1, le=5, description="Oda konforu/rahatlık (1-5)")
    value_for_money_score: int = Field(..., ge=1, le=5, description="Fiyat/performans değeri (1-5)")

    pros: list[str] = Field(
        ...,
        description="Otelin olumlu özellikleri",
    )
    cons: list[str] = Field(
        ...,
        description="Otelin olumsuz özellikleri",
    )
