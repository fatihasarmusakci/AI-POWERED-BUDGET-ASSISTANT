from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.db.base import Base


def _json_type() -> type[JSON | JSONB]:
    return JSON().with_variant(JSONB(), "postgresql")


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    persona_data: Mapped[dict[str, Any]] = mapped_column(_json_type(), nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    smart_scores: Mapped[list[SmartScore]] = relationship(back_populates="user")


class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    location: Mapped[str] = mapped_column(String(512), nullable=False)
    official_photos: Mapped[list[Any]] = mapped_column(_json_type(), nullable=False, default=list)
    external_api_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    reviews: Mapped[list[Review]] = relationship(back_populates="hotel", cascade="all, delete-orphan")
    smart_scores: Mapped[list[SmartScore]] = relationship(back_populates="hotel", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    hotel_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("hotels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    sentiment_scores: Mapped[dict[str, Any] | None] = mapped_column(_json_type(), nullable=True)
    source: Mapped[str] = mapped_column(String(64), nullable=False, default="booking")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    hotel: Mapped[Hotel] = relationship(back_populates="reviews")


class SmartScore(Base):
    __tablename__ = "smart_scores"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    hotel_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("hotels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    user_persona_type: Mapped[str] = mapped_column(String(128), nullable=False)
    score_value: Mapped[float] = mapped_column(nullable=False)
    category_breakdown: Mapped[dict[str, Any]] = mapped_column(_json_type(), nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    hotel: Mapped[Hotel] = relationship(back_populates="smart_scores")
    user: Mapped[User | None] = relationship(back_populates="smart_scores")
