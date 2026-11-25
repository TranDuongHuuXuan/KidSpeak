from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class AdminUserUpdateSchema(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = Field(default=None, max_length=255)
    avatar: str | None = Field(default=None, max_length=500)
    date_of_birth: datetime | None = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value):
        if value is None:
            return value
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Họ tên phải có ít nhất 2 ký tự.")
        return value

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, value):
        if value is None:
            return value
        return value.strip().lower() if isinstance(value, str) else value

    @field_validator("avatar")
    @classmethod
    def validate_avatar(cls, value):
        if value is None:
            return value
        value = value.strip()
        return value or None


class AdminUserResponseSchema(BaseModel):
    id: int
    full_name: str
    email: str
    role_id: int
    role_name: str
    date_of_birth: datetime | None = None
    avatar: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    specialty: str | None = None
    teaching_experience: str | None = None
    teacher_introduction: str | None = None
    course_enrollment_count: int | None = None
    practice_session_count: int | None = None
    practice_history_count: int | None = None

    model_config = ConfigDict(from_attributes=True)
