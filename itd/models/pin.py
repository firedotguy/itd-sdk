from datetime import datetime

from pydantic import BaseModel, Field

class ShortPin(BaseModel):
    slug: str
    name: str
    description: str


class Pin(ShortPin):
    granted_at: datetime = Field(alias='grantedAt')