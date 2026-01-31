from pydantic import BaseModel, Field


class Clan(BaseModel):
    avatar: str
    member_count: int = Field(0, alias='memberCount')