from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SendAdminExpertMessageSchema(BaseModel):
    content: str = Field(min_length=1, max_length=5000)

    model_config = ConfigDict(extra="forbid")

    @field_validator("content")
    @classmethod
    def trim_content(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Tin nhắn không được để trống.")
        return value


class AdminExpertMessageResponse(BaseModel):
    id: int
    conversation_id: int
    sender_id: int
    recipient_id: int
    content: str
    sent_at: datetime
    read_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
