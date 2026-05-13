from __future__ import annotations

import math
from typing import Any, Sequence

from app.models.orm import Hotel, Review
from app.services.nlp_service import extract_negative_visual_flags


def compute_visual_honesty(hotel: Hotel, reviews: Sequence[Review]) -> dict[str, Any]:
    official_count = len(hotel.official_photos or [])
    analyzed = [r for r in reviews if r.sentiment_scores]
    neg_visual = 0
    for r in analyzed:
        if extract_negative_visual_flags(r.sentiment_scores):
            neg_visual += 1
    review_count = len(reviews)
    ratio = neg_visual / max(1, len(analyzed) if analyzed else 1)
    transparency_boost = math.log1p(official_count) * 0.35
    penalty = ratio * 7.0
    raw = 6.5 + transparency_boost - penalty
    honesty = max(0.0, min(10.0, round(raw, 2)))
    rationale = (
        f"{official_count} resmi fotoğraf; {neg_visual}/{max(1, len(analyzed))} analiz edilmiş yorumda "
        f"olumsuz görsel/görünüm geri bildirimi. Şeffaflık artışı ve olumsuz görsel oranı birleştirildi."
    )
    return {
        "honesty_score": honesty,
        "official_photo_count": official_count,
        "negative_visual_mentions": neg_visual,
        "review_count": review_count,
        "rationale": rationale,
    }
