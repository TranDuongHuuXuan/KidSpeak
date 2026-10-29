from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# ── User response schema ──────────────────────────────────────────────────────
class UserSchema(BaseModel):
    """Response schema for user information — mapped from the User model."""

    id: int
    username: str
    email: str
    role_id: Optional[int] = None
    date_of_birth: Optional[datetime] = None
    avatar: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ── Minimal register response schema ─────────────────────────────────────────
class UserRegisterResponseSchema(BaseModel):
    """Slim response schema returned after registration — no sensitive fields."""

    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ── Login response schema ─────────────────────────────────────────────────────
class LoginResponseSchema(BaseModel):
    """Response schema returned after a successful login."""

    access_token: str
    token_type: str = "bearer"
    user: UserSchema

    class Config:
        from_attributes = True

class UserSchema(BaseModel):
    """Schema for user response (without password)."""

    id: int
    username: str
    email: str
    role_id: int | None = None
    date_of_birth: datetime | None = None
    avatar: str | None = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
