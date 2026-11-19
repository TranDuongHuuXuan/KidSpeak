from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# ── User response schema ──────────────────────────────────────────────────────
class UserSchema(BaseModel):
    """Response schema for user information — mapped from the User model."""

    id: int
    full_name: str
    email: str
    role_id: Optional[int] = None
    role_name: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    avatar: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Minimal register response schema ─────────────────────────────────────────
class UserRegisterResponseSchema(BaseModel):
    """Slim response schema returned after registration — no sensitive fields."""

    id: int
    full_name: str
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

    model_config = {"from_attributes": True}
