from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from itd.enums import AttachType

class File(BaseModel):
    id: UUID
    url: str
    filename: str
    mime_type: str = Field(alias='mimeType')
    size: int
    created_at: datetime | None = Field(None, alias='createdAt')


class PostAttach(BaseModel):
    id: UUID
    type: AttachType = AttachType.IMAGE
    url: str
    thumbnail_url: str | None = Field(None, alias='thumbnailUrl')
    width: int | None = None
    height: int | None = None


class Attach(PostAttach):
    filename: str
    mime_type: str = Field(alias='mimeType')
    size: int
    duration: int | None = None
    order: int = 0