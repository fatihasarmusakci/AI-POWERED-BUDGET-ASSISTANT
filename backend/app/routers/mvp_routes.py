from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.schemas.mvp import (
    AiGenerateRequest,
    AiGenerateResponse,
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    SavedGeneration,
)

router = APIRouter(prefix="/mvp", tags=["mvp-boilerplate"])

# NOTE: 8 haftalık MVP başlangıcı için geçici in-memory depolama.
# Production aşamasında PostgreSQL + gerçek auth (JWT + refresh token) ile değiştirilmelidir.
_users_by_email: dict[str, dict[str, str]] = {}
_token_to_user_id: dict[str, str] = {}
_saved_generations: list[SavedGeneration] = []


def _require_user_id(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header eksik veya geçersiz.",
        )
    token = authorization.split(" ", 1)[1].strip()
    user_id = _token_to_user_id.get(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token geçersiz.",
        )
    return user_id


@router.post("/auth/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest) -> AuthResponse:
    if payload.email in _users_by_email:
        raise HTTPException(status_code=409, detail="Bu e-posta zaten kayıtlı.")

    user_id = f"user_{uuid4().hex[:10]}"
    _users_by_email[payload.email] = {
        "id": user_id,
        "email": payload.email,
        # MVP boilerplate: hash yerine düz saklama var; production için değiştirin.
        "password": payload.password,
        "full_name": payload.full_name,
    }
    token = f"dev_{uuid4().hex}"
    _token_to_user_id[token] = user_id
    return AuthResponse(access_token=token, user_id=user_id, email=payload.email)


@router.post("/auth/login", response_model=AuthResponse)
def login(payload: LoginRequest) -> AuthResponse:
    user = _users_by_email.get(payload.email)
    if not user or user["password"] != payload.password:
        raise HTTPException(status_code=401, detail="E-posta veya şifre hatalı.")

    token = f"dev_{uuid4().hex}"
    _token_to_user_id[token] = user["id"]
    return AuthResponse(access_token=token, user_id=user["id"], email=user["email"])


@router.post("/ai/generate", response_model=AiGenerateResponse)
def generate_with_ai(
    payload: AiGenerateRequest,
    user_id: str = Depends(_require_user_id),
) -> AiGenerateResponse:
    _ = user_id
    # TODO: Burayı Gemini/OpenRouter/OpenAI sunucu tarafı çağrısıyla değiştirin.
    output = (
        "MVP yanıtı: Girdi başarıyla alındı. "
        "Bir sonraki adımda bu noktaya gerçek LLM entegrasyonu bağlanacak.\n\n"
        f"Prompt özeti: {payload.prompt[:180]}"
    )
    return AiGenerateResponse(output=output, provider="mock", model="mvp-boilerplate")


@router.post("/generations", response_model=SavedGeneration, status_code=status.HTTP_201_CREATED)
def save_generation(
    payload: AiGenerateResponse,
    user_id: str = Depends(_require_user_id),
) -> SavedGeneration:
    item = SavedGeneration(
        id=f"gen_{uuid4().hex[:10]}",
        user_id=user_id,
        prompt="saved-from-client",
        output=payload.output,
        created_at=datetime.now(timezone.utc),
    )
    _saved_generations.append(item)
    return item


@router.get("/generations", response_model=list[SavedGeneration])
def list_generations(user_id: str = Depends(_require_user_id)) -> list[SavedGeneration]:
    return [item for item in _saved_generations if item.user_id == user_id]
