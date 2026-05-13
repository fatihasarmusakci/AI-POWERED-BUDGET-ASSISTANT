from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session
from app.core.exceptions import NotFoundError
from app.repositories import (
    HotelRepository,
    ReviewRepository,
    SmartScoreRepository,
    UserRepository,
)
from app.schemas.api import (
    HotelCard,
    HotelListResponse,
    HotelTLDRResponse,
    SmartScoreResponse,
    SummaryResponse,
    TruthMedia,
    TruthResponse,
    VisualHonestyResponse,
)
from app.services.honesty_service import compute_visual_honesty
from app.services.scoring_service import (
    average_category_scores,
    compute_smart_score_value,
    derive_persona_label,
)
from app.services.summarization_service import SummarizationService

router = APIRouter(prefix="/hotels", tags=["hotels"])


def _parse_uuid(value: str, *, label: str) -> uuid.UUID:
    try:
        return uuid.UUID(value)
    except ValueError as exc:
        raise NotFoundError(f"Invalid {label}") from exc


def _district(location: str) -> str:
    parts = [p.strip() for p in location.split(",") if p.strip()]
    return parts[-1] if parts else location


def _vibe_tags(avgs: dict[str, float]) -> list[str]:
    tags: list[str] = []
    if avgs.get("sessizlik_skoru", 5.0) >= 7.5:
        tags.append("quiet")
    if avgs.get("sessizlik_skoru", 5.0) <= 5.5:
        tags.append("lively")
    if avgs.get("konum_skoru", 5.0) >= 7.5:
        tags.append("metro")
    if avgs.get("hizmet_skoru", 5.0) >= 7.5:
        tags.append("service")
    return tags or ["balanced"]


def _card_smart_score(reviews: list) -> float:
    analyses = [r.sentiment_scores for r in reviews if r.sentiment_scores]
    avgs = average_category_scores(analyses)
    score, _ = compute_smart_score_value({}, avgs)
    return score


@router.get("", response_model=HotelListResponse)
async def list_hotels(
    city: str = Query(default="london"),
    session: AsyncSession = Depends(get_db_session),
) -> HotelListResponse:
    hotels_repo = HotelRepository(session)
    rows = await hotels_repo.search_by_location_contains(city)
    items: list[HotelCard] = []
    for hotel in rows:
        analyses = [r.sentiment_scores for r in hotel.reviews if r.sentiment_scores]
        avgs = average_category_scores(analyses)
        items.append(
            HotelCard(
                id=str(hotel.id),
                name=hotel.name,
                district=_district(hotel.location),
                smart_score=_card_smart_score(list(hotel.reviews)),
                vibe_tags=_vibe_tags(avgs),
            )
        )
    return HotelListResponse(city=city, items=items)


@router.get("/{hotel_id}/truth", response_model=TruthResponse)
async def get_truth(
    hotel_id: str,
    session: AsyncSession = Depends(get_db_session),
) -> TruthResponse:
    hid = _parse_uuid(hotel_id, label="hotel id")
    hotels_repo = HotelRepository(session)
    reviews_repo = ReviewRepository(session)
    hotel = await hotels_repo.get_by_id(hid)
    if hotel is None:
        raise NotFoundError("Hotel not found")
    reviews = await reviews_repo.list_for_hotel(hid)
    honesty = compute_visual_honesty(hotel, list(reviews))
    red_flags: list[str] = []
    if honesty["negative_visual_mentions"] > 0:
        red_flags.append(
            f"{honesty['negative_visual_mentions']} yorumda olumsuz görsel/görünüm geri bildirimi"
        )
    if len(hotel.official_photos or []) >= 8:
        red_flags.append("Çok sayıda resmi fotoğraf — şeffaflık sinyali yüksek")
    if not red_flags:
        red_flags.append("Belirgin kırmızı bayrak bulunamadı (heuristik)")
    compare = TruthMedia(
        official_label="Resmi oda galerisi",
        official_date="2025-01-10",
        user_label="Kullanıcı gerçekliği (yorum metinleri)",
        user_date="2026-05-13",
    )
    return TruthResponse(hotel_id=str(hid), compare=compare, red_flags=red_flags)


@router.get("/{hotel_id}/summary", response_model=SummaryResponse)
async def get_summary(
    hotel_id: str,
    session: AsyncSession = Depends(get_db_session),
) -> SummaryResponse:
    hid = _parse_uuid(hotel_id, label="hotel id")
    reviews_repo = ReviewRepository(session)
    hotel_repo = HotelRepository(session)
    hotel = await hotel_repo.get_by_id(hid)
    if hotel is None:
        raise NotFoundError("Hotel not found")
    reviews = list(await reviews_repo.list_for_hotel(hid))
    summarizer = SummarizationService()
    bullets, _model = summarizer.build_three_bullets(reviews)
    text = "\n".join(f"- {b}" for b in bullets[:3])
    return SummaryResponse(
        hotel_id=str(hid),
        review_count=len(reviews),
        summary=text,
        cache_window="daily",
    )


@router.get("/{hotel_id}/tldr", response_model=HotelTLDRResponse)
async def get_hotel_tldr(
    hotel_id: str,
    session: AsyncSession = Depends(get_db_session),
) -> HotelTLDRResponse:
    hid = _parse_uuid(hotel_id, label="hotel id")
    reviews_repo = ReviewRepository(session)
    hotel_repo = HotelRepository(session)
    hotel = await hotel_repo.get_by_id(hid)
    if hotel is None:
        raise NotFoundError("Hotel not found")
    reviews = list(await reviews_repo.list_for_hotel(hid))
    summarizer = SummarizationService()
    bullets, model_used = summarizer.build_three_bullets(reviews)
    return HotelTLDRResponse(
        hotel_id=hid,
        bullets=bullets[:3],
        review_count=len(reviews),
        model_used=model_used,
    )


@router.get("/{hotel_id}/smart-score", response_model=SmartScoreResponse)
async def get_smart_score(
    hotel_id: str,
    user_id: uuid.UUID = Query(..., description="Persona ağırlıkları için kullanıcı id"),
    persist: bool = Query(default=False, description="True ise SmartScore tablosuna kaydeder"),
    session: AsyncSession = Depends(get_db_session),
) -> SmartScoreResponse:
    hid = _parse_uuid(hotel_id, label="hotel id")
    hotels_repo = HotelRepository(session)
    users_repo = UserRepository(session)
    reviews_repo = ReviewRepository(session)
    scores_repo = SmartScoreRepository(session)

    hotel = await hotels_repo.get_by_id(hid)
    if hotel is None:
        raise NotFoundError("Hotel not found")
    user = await users_repo.get_by_id(user_id)
    if user is None:
        raise NotFoundError("User not found")

    reviews = list(await reviews_repo.list_for_hotel(hid))
    analyses = [r.sentiment_scores for r in reviews if r.sentiment_scores]
    avgs = average_category_scores(analyses)
    persona = user.persona_data if isinstance(user.persona_data, dict) else {}
    score_value, breakdown = compute_smart_score_value(persona, avgs)
    label = derive_persona_label(persona)
    persisted = False
    if persist:
        await scores_repo.create(
            hotel_id=hid,
            user_id=user_id,
            user_persona_type=label,
            score_value=score_value,
            category_breakdown=breakdown,
        )
        persisted = True
        await session.commit()
    return SmartScoreResponse(
        hotel_id=hid,
        user_id=user_id,
        user_persona_type=label,
        score_value=score_value,
        category_breakdown=breakdown,
        persisted=persisted,
    )


@router.get("/{hotel_id}/visual-honesty", response_model=VisualHonestyResponse)
async def get_visual_honesty(
    hotel_id: str,
    session: AsyncSession = Depends(get_db_session),
) -> VisualHonestyResponse:
    hid = _parse_uuid(hotel_id, label="hotel id")
    hotels_repo = HotelRepository(session)
    reviews_repo = ReviewRepository(session)
    hotel = await hotels_repo.get_by_id(hid)
    if hotel is None:
        raise NotFoundError("Hotel not found")
    reviews = list(await reviews_repo.list_for_hotel(hid))
    payload = compute_visual_honesty(hotel, reviews)
    return VisualHonestyResponse(hotel_id=hid, **payload)
