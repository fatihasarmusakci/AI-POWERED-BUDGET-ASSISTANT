"""Re-export schemas for legacy imports (`app.models.schemas`)."""

from app.schemas.api import (
    DailyInsightResponse,
    GameGuessRequest,
    GameGuessResponse,
    HealthResponse,
    HotelCard,
    HotelListResponse,
    MapPin,
    StaycationRatingRequest,
    StaycationRatingResponse,
    SummaryResponse,
    TruthMedia,
    TruthResponse,
    VibeMapResponse,
)

__all__ = [
    "HealthResponse",
    "HotelCard",
    "HotelListResponse",
    "TruthMedia",
    "TruthResponse",
    "SummaryResponse",
    "MapPin",
    "VibeMapResponse",
    "GameGuessRequest",
    "GameGuessResponse",
    "DailyInsightResponse",
    "StaycationRatingRequest",
    "StaycationRatingResponse",
]
