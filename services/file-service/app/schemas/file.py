from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FileResponse(BaseModel):
    id: int
    filename: str
    object_name: str
    content_type: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)