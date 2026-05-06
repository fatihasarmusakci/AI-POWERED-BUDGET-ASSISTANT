from fastapi import APIRouter, Query

from app.models.schemas import (
    DailyInsightResponse,
    GameGuessRequest,
    GameGuessResponse,
    StaycationRatingRequest,
    StaycationRatingResponse,
)

router = APIRouter(tags=["engagement"])


@router.post("/game/guess", response_model=GameGuessResponse)
def submit_game_guess(payload: GameGuessRequest) -> GameGuessResponse:
    if payload.guess not in {"real", "manipulated"}:
        return GameGuessResponse(
            accepted=False,
            message="guess must be one of: real, manipulated",
        )
    return GameGuessResponse(accepted=True, message="guess accepted")


@router.get("/insights/daily", response_model=DailyInsightResponse)
def get_daily_insight(city: str = Query(default="london")) -> DailyInsightResponse:
    return DailyInsightResponse(
        city=city,
        title="Local honest recommendation",
        message="Best breakfast workspace today is in Soho between 08:00 and 10:00.",
    )


@router.post("/staycation/rating", response_model=StaycationRatingResponse)
def submit_staycation_rating(
    payload: StaycationRatingRequest,
) -> StaycationRatingResponse:
    average_score = round(
        (payload.coworking_score + payload.brunch_score + payload.wifi_score) / 3,
        2,
    )
    return StaycationRatingResponse(accepted=True, average_score=average_score)
