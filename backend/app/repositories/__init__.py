from __future__ import annotations

import uuid
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.orm import Hotel, Review, SmartScore, User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        result = await self._session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        result = await self._session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def create(self, username: str, persona_data: dict) -> User:
        user = User(username=username, persona_data=persona_data)
        self._session.add(user)
        await self._session.flush()
        await self._session.refresh(user)
        return user

    async def list_all(self, *, limit: int = 50) -> Sequence[User]:
        stmt = select(User).order_by(User.username).limit(limit)
        result = await self._session.execute(stmt)
        return result.scalars().all()


class HotelRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, hotel_id: uuid.UUID) -> Hotel | None:
        result = await self._session.execute(select(Hotel).where(Hotel.id == hotel_id))
        return result.scalar_one_or_none()

    async def get_by_id_with_reviews(self, hotel_id: uuid.UUID) -> Hotel | None:
        stmt = (
            select(Hotel)
            .options(selectinload(Hotel.reviews))
            .where(Hotel.id == hotel_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> Sequence[Hotel]:
        result = await self._session.execute(select(Hotel).order_by(Hotel.name))
        return result.scalars().all()

    async def search_by_location_contains(self, needle: str) -> Sequence[Hotel]:
        pattern = f"%{needle.lower()}%"
        stmt = (
            select(Hotel)
            .options(selectinload(Hotel.reviews))
            .where(func.lower(Hotel.location).like(pattern))
            .order_by(Hotel.name)
        )
        result = await self._session.execute(stmt)
        return result.scalars().unique().all()


class ReviewRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        hotel_id: uuid.UUID,
        raw_text: str,
        source: str,
    ) -> Review:
        review = Review(hotel_id=hotel_id, raw_text=raw_text, source=source, sentiment_scores=None)
        self._session.add(review)
        await self._session.flush()
        await self._session.refresh(review)
        return review

    async def get_by_id(self, review_id: uuid.UUID) -> Review | None:
        result = await self._session.execute(select(Review).where(Review.id == review_id))
        return result.scalar_one_or_none()

    async def list_for_hotel(self, hotel_id: uuid.UUID) -> Sequence[Review]:
        stmt = select(Review).where(Review.hotel_id == hotel_id).order_by(Review.created_at.desc())
        result = await self._session.execute(stmt)
        return result.scalars().all()


class SmartScoreRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        hotel_id: uuid.UUID,
        user_id: uuid.UUID | None,
        user_persona_type: str,
        score_value: float,
        category_breakdown: dict,
    ) -> SmartScore:
        row = SmartScore(
            hotel_id=hotel_id,
            user_id=user_id,
            user_persona_type=user_persona_type,
            score_value=score_value,
            category_breakdown=category_breakdown,
        )
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return row
