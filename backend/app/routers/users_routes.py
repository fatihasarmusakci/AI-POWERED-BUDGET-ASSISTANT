from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session
from app.core.exceptions import ConflictError, NotFoundError
from app.repositories import UserRepository
from app.schemas.api import UserCreateRequest, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
async def list_users(
    limit: int = Query(default=50, ge=1, le=200),
    session: AsyncSession = Depends(get_db_session),
) -> list[UserResponse]:
    repo = UserRepository(session)
    users = await repo.list_all(limit=limit)
    return [UserResponse(id=u.id, username=u.username, persona_data=dict(u.persona_data)) for u in users]


@router.post("", response_model=UserResponse, status_code=201)
async def create_user(
    payload: UserCreateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> UserResponse:
    repo = UserRepository(session)
    existing = await repo.get_by_username(payload.username)
    if existing is not None:
        raise ConflictError("Username already taken")
    user = await repo.create(payload.username, dict(payload.persona_data))
    await session.commit()
    return UserResponse(id=user.id, username=user.username, persona_data=dict(user.persona_data))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
) -> UserResponse:
    repo = UserRepository(session)
    user = await repo.get_by_id(user_id)
    if user is None:
        raise NotFoundError("User not found")
    return UserResponse(id=user.id, username=user.username, persona_data=dict(user.persona_data))
