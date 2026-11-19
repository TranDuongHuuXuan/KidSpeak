from typing import Literal

from pydantic import BaseModel


class MediaObjectSchema(BaseModel):
    object_key: str
    filename: str
    content_type: str
    media_type: Literal["image", "audio"]
    file_size: int
    url: str
    format: str | None = None
    duration: float | None = None
    sample_rate: int | None = None
    channels: int | None = None


class UserAvatarSchema(BaseModel):
    object_key: str
    url: str
