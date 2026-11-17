from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas.user_schema import UserSchema


# ── Register schema ───────────────────────────────────────────────────────────
class RegisterSchema(BaseModel):
    """Input data for new user registration."""

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name (2–100 characters)",
    )
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="Password (8–72 characters, mixed case, digit, and symbol)",
    )
    date_of_birth: date = Field(
        ...,
        description="Date of birth in YYYY-MM-DD format",
    )

    @field_validator("full_name", mode="before")
    @classmethod
    def full_name_not_blank(cls, value: str) -> str:
        if not isinstance(value, str):
            return value
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Full name must contain at least 2 characters")
        return value

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password must not exceed 72 UTF-8 bytes")
        if not any("a" <= c <= "z" for c in v):
            raise ValueError("Password must contain a lowercase letter")
        if not any("A" <= c <= "Z" for c in v):
            raise ValueError("Password must contain an uppercase letter")
        if not any("0" <= c <= "9" for c in v):
            raise ValueError("Password must contain a digit")
        if not any(not (c.isascii() and c.isalnum()) for c in v):
            raise ValueError("Password must contain a symbol")
        return v

    @field_validator("date_of_birth")
    @classmethod
    def date_of_birth_not_in_future(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return value


# ── Login schema ──────────────────────────────────────────────────────────────
class LoginSchema(BaseModel):
    """Input data for user login."""

    email: EmailStr = Field(..., description="Registered email")
    password: str = Field(..., min_length=1, description="Password")


# ── OTP verification schema ───────────────────────────────────────────────────
class VerifyOTPSchema(BaseModel):
    """OTP verification data sent via email."""

    email: EmailStr = Field(..., description="Registered email")
    otp: str = Field(..., min_length=4, max_length=10, description="OTP code")

class LoginResponseSchema(BaseModel):
    access_token: str
    user_principal: UserSchema

    class Config:
        from_attributes = True