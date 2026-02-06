from typing import List, Optional
from pydantic import BaseModel
from iter.types.content import Post
from iter.types.user import User

class Pagination(BaseModel):
    limit: int
    nextCursor: Optional[str] = None
    hasMore: bool

class FeedData(BaseModel):
    posts: List[Post]
    pagination: Pagination

class Hashtag(BaseModel):
    id: str
    name: str
    postsCount: int

class SearchData(BaseModel):
    users: List[User] = []
    hashtags: List[Hashtag] = []