from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from itd.models.user import UserPost


class TextObject(BaseModel):
    id: UUID
    content: str
    author: UserPost
    attachments: list[UUID]

    created_at: datetime = Field(alias='createdAt')

    model_config = {'populate_by_name': True}