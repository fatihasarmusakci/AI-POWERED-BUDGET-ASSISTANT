from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session
from app.core.config import settings
from app.core.exceptions import NotFoundError
from app.repositories import HotelRepository, ReviewRepository
from app.schemas.api import ReviewCreateRequest, ReviewResponse
from app.workers.tasks import analyze_review_task

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("", response_model=ReviewResponse, status_code=201)
async def create_review(
    payload: ReviewCreateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> ReviewResponse:
    hotels_repo = HotelRepository(session)
    reviews_repo = ReviewRepository(session)
    hotel = await hotels_repo.get_by_id(payload.hotel_id)
    if hotel is None:
        raise NotFoundError("Hotel not found")
    review = await reviews_repo.create(
        hotel_id=payload.hotel_id,
        raw_text=payload.raw_text,
        source=payload.source,
    )
    await session.commit()
    analyze_review_task.delay(str(review.id))
    if settings.celery_eager:
        await session.refresh(review)
    return ReviewResponse(
        id=review.id,
        hotel_id=review.hotel_id,
        raw_text=review.raw_text,
        sentiment_scores=review.sentiment_scores,
        source=review.source,
        analysis_complete=review.sentiment_scores is not None,
    )
