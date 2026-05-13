from __future__ import annotations

import logging
import uuid

from sqlalchemy import select

from app.db.session import SyncSessionLocal
from app.models.orm import Review
from app.services.nlp_service import NLPService
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="reviews.analyze_review")
def analyze_review_task(review_id: str) -> None:
    rid = uuid.UUID(review_id)
    nlp = NLPService()
    with SyncSessionLocal() as session:
        review = session.execute(select(Review).where(Review.id == rid)).scalar_one_or_none()
        if review is None:
            logger.warning("Review %s not found for NLP task", review_id)
            return
        scores = nlp.analyze_review_text(review.raw_text)
        review.sentiment_scores = scores
        session.add(review)
        session.commit()
