from fastapi import APIRouter, Query

from app.models.schemas import (
    HotelCard,
    HotelListResponse,
    SummaryResponse,
    TruthMedia,
    TruthResponse,
)

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("", response_model=HotelListResponse)
def list_hotels(city: str = Query(default="london")) -> HotelListResponse:
    items = [
        HotelCard(
            id="camden-loft",
            name="Camden Loft Hotel",
            district="Camden",
            smart_score=8.4,
            vibe_tags=["party", "metro"],
        ),
        HotelCard(
            id="shoreditch-stay",
            name="Shoreditch Stay",
            district="Shoreditch",
            smart_score=8.8,
            vibe_tags=["quiet", "coworking"],
        ),
    ]
    return HotelListResponse(city=city, items=items)


@router.get("/{hotel_id}/truth", response_model=TruthResponse)
def get_truth(hotel_id: str) -> TruthResponse:
    compare = TruthMedia(
        official_label="Official room gallery",
        official_date="2025-01-10",
        user_label="User uploaded room reality",
        user_date="2026-04-21",
    )
    return TruthResponse(
        hotel_id=hotel_id,
        compare=compare,
        red_flags=["4 same-IP reviews", "3 near-duplicate praise comments"],
    )


@router.get("/{hotel_id}/summary", response_model=SummaryResponse)
def get_summary(hotel_id: str) -> SummaryResponse:
    return SummaryResponse(
        hotel_id=hotel_id,
        review_count=24,
        summary="Pros: stable Wi-Fi and coffee quality. Cons: slow elevator. Vibe: industrial and young.",
        cache_window="weekly",
    )
