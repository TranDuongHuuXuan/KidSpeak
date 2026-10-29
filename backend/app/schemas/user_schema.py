from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


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
