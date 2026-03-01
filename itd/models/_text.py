from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class TextObject(BaseModel):
    id: UUID
    content: str

    created_at: datetime = Field(alias='createdAt')

    model_config = {'populate_by_name': True}

    @field_validator('created_at', mode='plain')
    @classmethod
    def validate_created_at(cls, v: str):
        v = v.replace('Z', '+00:00')
        try:
            return datetime.strptime(v + '00', '%Y-%m-%d %H:%M:%S.%f%z')
        except ValueError:
            return datetime.fromisoformat(v)