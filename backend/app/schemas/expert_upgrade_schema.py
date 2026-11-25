from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user_schema import UserSchema


class ExpertUpgradeInput(BaseModel):
    specialty: str = Field(default="", max_length=120)
    experience: str = Field(default="", max_length=4000)
    reason: str = Field(min_length=1, max_length=2000)
    introduction: str = Field(default="", max_length=2000)


class ExpertUpgradeDocument(BaseModel):
    file_name: str
    file_key: str
    file_type: str
    file_size: int
    uploaded_at: datetime | None = None


class ExpertUpgradeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    specialty: str
    experience: str
    reason: str
    introduction: str
    documents: list[ExpertUpgradeDocument]
    status: Literal["pending", "approved", "rejected", "activated"]
    review_note: str
    reviewed_by: int | None
    submitted_at: datetime
    reviewed_at: datetime | None
    activated_at: datetime | None = None


class AdminExpertUpgradeResponse(ExpertUpgradeResponse):
    applicant_name: str
    applicant_email: str
    applicant: UserSchema
    reviewer_name: str | None = None
    applicant_avatar_url: str | None = None


class ExpertUpgradeReviewInput(BaseModel):
    status: Literal["approved", "rejected"]
    review_note: str = Field(default="", max_length=2000)
