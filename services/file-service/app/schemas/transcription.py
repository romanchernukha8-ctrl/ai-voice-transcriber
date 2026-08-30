from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TranscriptionResponse(BaseModel):
    id: int
    file_id: int
    text: str
    language: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
