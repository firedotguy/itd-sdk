from pydantic import BaseModel
from typing import Optional

class Hashtag(BaseModel):
    id: str
    name: str
    postsCount: int

class CursorPagination(BaseModel):
    limit: int
    nextCursor: Optional[str] = None
    hasMore: bool

class PagePagination(BaseModel):
    page: int
    limit: int
    total: int
    hasMore: bool