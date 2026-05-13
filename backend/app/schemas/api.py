from __future__ import annotations

import uuid
from typing import Any, Literal

from pydantic import BaseModel, Field

ReviewSource = Literal["booking", "tripadvisor", "other"]


class ErrorResponse(BaseModel):
    detail: str
    code: str


class HealthResponse(BaseModel):
    status: str = Field(examples=["ok"])
    service: str = Field(examples=["vibecheck-api"])


class PersonaWeights(BaseModel):
    temizlik: float = Field(default=0.25, ge=0.0, le=1.0)
    sessizlik: float = Field(default=0.25, ge=0.0, le=1.0)
    hizmet: float = Field(default=0.25, ge=0.0, le=1.0)
    konum: float = Field(default=0.25, ge=0.0, le=1.0)


class PersonaData(BaseModel):
    """Structured view; extra keys are allowed at API boundary via dict merge in service."""

    weights: PersonaWeights | None = None
    titizlik: float | None = Field(default=None, ge=0.0, le=1.0)
    sessizlik_tercihi: float | None = Field(
        default=None,
        description="0-1 how much user cares about quiet; boosts sessizlik weight when weights omitted.",
        ge=0.0,
        le=1.0,
    )

    model_config = {"extra": "allow"}


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=2, max_length=255)
    persona_data: dict[str, Any] = Field(default_factory=dict)


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    persona_data: dict[str, Any]

    model_config = {"from_attributes": True}


class HotelCard(BaseModel):
    id: str
    name: str
    district: str
    smart_score: float
    vibe_tags: list[str]


class HotelListResponse(BaseModel):
    city: str
    items: list[HotelCard]


class HotelResponse(BaseModel):
    id: uuid.UUID
    name: str
    location: str
    official_photos: list[str]
    external_api_id: str | None

    model_config = {"from_attributes": True}


class ReviewCreateRequest(BaseModel):
    hotel_id: uuid.UUID
    raw_text: str = Field(min_length=4, max_length=20_000)
    source: ReviewSource = "booking"


class ReviewResponse(BaseModel):
    id: uuid.UUID
    hotel_id: uuid.UUID
    raw_text: str
    sentiment_scores: dict[str, Any] | None
    source: str
    analysis_complete: bool


class NLPScoresPayload(BaseModel):
    temizlik_skoru: int = Field(ge=1, le=10)
    sessizlik_skoru: int = Field(ge=1, le=10)
    hizmet_skoru: int = Field(ge=1, le=10)
    konum_skoru: int = Field(ge=1, le=10)
    temizlik_insight: str
    sessizlik_insight: str
    hizmet_insight: str
    konum_insight: str
    gorsel_sikayet_negatif: bool = False
    gorsel_sikayet_ozeti: str | None = None


class SmartScoreCategoryBreakdown(BaseModel):
    temizlik_skoru: float
    gurultu_skoru: float
    hizmet_skoru: float
    konum_skoru: float


class SmartScoreResponse(BaseModel):
    hotel_id: uuid.UUID
    user_id: uuid.UUID | None
    user_persona_type: str
    score_value: float
    category_breakdown: dict[str, Any]
    persisted: bool = Field(
        default=False,
        description="True if a new SmartScore row was written for this computation.",
    )


class VisualHonestyResponse(BaseModel):
    hotel_id: uuid.UUID
    honesty_score: float = Field(ge=0.0, le=10.0)
    official_photo_count: int
    negative_visual_mentions: int
    review_count: int
    rationale: str


class HotelTLDRResponse(BaseModel):
    hotel_id: uuid.UUID
    bullets: list[str] = Field(min_length=1, max_length=10)
    review_count: int
    model_used: str | None = None


class TruthMedia(BaseModel):
    official_label: str
    official_date: str
    user_label: str
    user_date: str


class TruthResponse(BaseModel):
    hotel_id: str
    compare: TruthMedia
    red_flags: list[str]


class SummaryResponse(BaseModel):
    hotel_id: str
    review_count: int
    summary: str
    cache_window: str


class MapPin(BaseModel):
    id: str
    label: str
    layers: list[str]


class VibeMapResponse(BaseModel):
    city: str
    layers: list[str]
    pins: list[MapPin]


class GameGuessRequest(BaseModel):
    prompt_id: str
    guess: str


class GameGuessResponse(BaseModel):
    accepted: bool
    message: str


class DailyInsightResponse(BaseModel):
    city: str
    title: str
    message: str


class StaycationRatingRequest(BaseModel):
    venue_id: str
    coworking_score: float
    brunch_score: float
    wifi_score: float


class StaycationRatingResponse(BaseModel):
    accepted: bool
    average_score: float
