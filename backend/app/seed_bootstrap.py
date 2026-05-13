from __future__ import annotations

from typing import Any

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.orm import Hotel, Review, SmartScore, User


def _static_sentiment(
    *,
    temizlik: int,
    sessizlik: int,
    hizmet: int,
    konum: int,
    visual_neg: bool = False,
) -> dict[str, Any]:
    return {
        "temizlik_skoru": temizlik,
        "sessizlik_skoru": sessizlik,
        "hizmet_skoru": hizmet,
        "konum_skoru": konum,
        "temizlik_insight": "Seed verisi: temizlik izlenimi.",
        "sessizlik_insight": "Seed verisi: sessizlik izlenimi.",
        "hizmet_insight": "Seed verisi: hizmet izlenimi.",
        "konum_insight": "Seed verisi: konum izlenimi.",
        "gorsel_sikayet_negatif": visual_neg,
        "gorsel_sikayet_ozeti": "Resmi fotoğraflar gerçek odayı yansıtmıyor." if visual_neg else None,
    }


async def _insert_demo_rows(session: AsyncSession) -> None:
    user = User(
        username="demo_quiet_guest",
        persona_data={
            "titizlik": 0.8,
            "sessizlik_tercihi": 0.9,
        },
    )
    session.add(user)

    h1 = Hotel(
        name="Camden Loft Hotel",
        location="London, Camden",
        official_photos=["https://example.com/camden/1.jpg", "https://example.com/camden/2.jpg"],
        external_api_id="ext-camden-loft",
    )
    h2 = Hotel(
        name="Shoreditch Stay",
        location="London, Shoreditch",
        official_photos=["https://example.com/shoreditch/a.jpg"],
        external_api_id="ext-shoreditch-stay",
    )
    session.add_all([h1, h2])
    await session.flush()

    reviews_payload: list[dict[str, Any]] = [
        {
            "hotel": h1,
            "text": "Temiz ama gece sokak gürültüsü çok geliyor, personel ilgili.",
            "source": "booking",
            "sentiment": _static_sentiment(temizlik=8, sessizlik=4, hizmet=8, konum=7),
        },
        {
            "hotel": h1,
            "text": "Oda fotoğraflarından daha küçük hissettirdi, banyoda küf kokusu.",
            "source": "tripadvisor",
            "sentiment": _static_sentiment(temizlik=5, sessizlik=6, hizmet=6, konum=6, visual_neg=True),
        },
        {
            "hotel": h2,
            "text": "Sakin bir sokak, kahvaltı harika, coworking alanı geniş.",
            "source": "booking",
            "sentiment": _static_sentiment(temizlik=9, sessizlik=9, hizmet=8, konum=7),
        },
    ]

    for row in reviews_payload:
        session.add(
            Review(
                hotel_id=row["hotel"].id,
                raw_text=row["text"],
                source=row["source"],
                sentiment_scores=row["sentiment"],
            )
        )

    await session.commit()


async def seed_demo_if_empty(session: AsyncSession) -> None:
    total_hotels = await session.scalar(select(func.count()).select_from(Hotel))
    if total_hotels and total_hotels > 0:
        return
    await _insert_demo_rows(session)


async def wipe_and_seed(session: AsyncSession) -> None:
    await session.execute(delete(Review))
    await session.execute(delete(SmartScore))
    await session.execute(delete(Hotel))
    await session.execute(delete(User))
    await session.commit()
    await _insert_demo_rows(session)
