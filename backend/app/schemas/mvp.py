from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=120)


class LoginRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str


class AiGenerateRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=2500)
    context: str | None = Field(default=None, max_length=2500)


class AiGenerateResponse(BaseModel):
    output: str
    provider: str
    model: str


class SavedGeneration(BaseModel):
    id: str
    user_id: str
    prompt: str
    output: str
    created_at: datetime
