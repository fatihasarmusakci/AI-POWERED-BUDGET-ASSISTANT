from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(examples=["ok"])
    service: str = Field(examples=["vibecheck-api"])


class HotelCard(BaseModel):
    id: str
    name: str
    district: str
    smart_score: float
    vibe_tags: list[str]


class HotelListResponse(BaseModel):
    city: str
    items: list[HotelCard]


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
