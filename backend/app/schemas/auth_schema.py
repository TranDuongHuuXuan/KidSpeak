from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


# ── Register schema ───────────────────────────────────────────────────────────
class RegisterSchema(BaseModel):
    """Input data for new user registration."""

    username: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Username (3–100 characters)",
    )
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(
        ...,
        min_length=6,
        max_length=255,
        description="Password (minimum 6 characters)",
    )
    date_of_birth: Optional[str] = Field(
        None,
        description="Date of birth in YYYY-MM-DD format (optional)",
    )

    @field_validator("username")
    @classmethod
    def username_no_space(cls, v: str) -> str:
        if " " in v:
            raise ValueError("Username must not contain spaces")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


# ── Login schema ──────────────────────────────────────────────────────────────
class LoginSchema(BaseModel):
    """Input data for user login."""

    email: EmailStr = Field(..., description="Registered email")
    password: str = Field(..., description="Password")


# ── OTP verification schema ───────────────────────────────────────────────────
class VerifyOTPSchema(BaseModel):
    """OTP verification data sent via email."""

    email: EmailStr = Field(..., description="Registered email")
    otp: str = Field(..., min_length=4, max_length=10, description="OTP code")
