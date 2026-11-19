from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

LessonLevel = Literal["BEGINNER", "INTERMEDIATE", "ADVANCED"]


class LessonCategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    image: str | None
    order: int
    created_at: datetime
    updated_at: datetime


class LessonResponse(BaseModel):
    id: int
    category_id: int | None
    category_name: str | None
    created_by: int | None
    creator_name: str | None
    title: str
    description: str | None
    level: LessonLevel | None
    order: int
    image: str | None
    is_published: bool
    created_at: datetime
    updated_at: datetime


class LessonCategoryInput(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    order: int = Field(default=0, ge=0)


class LessonInput(BaseModel):
    category_id: int
    title: str = Field(min_length=1, max_length=300)
    description: str | None = None
    level: LessonLevel
    order: int = Field(default=0, ge=0)
    is_published: bool = True
