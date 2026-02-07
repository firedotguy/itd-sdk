from __future__ import annotations
from typing import Optional
from .base import IterBaseModel, PostgresDateTime

class User(IterBaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    display_name: str
    avatar: str
    verified: bool = False
    followers_count: Optional[int] = 0

class UserFull(User):
    banner: Optional[str] = None
    bio: Optional[str] = None
    pin: Optional[str] = None
    pinned_post_id: Optional[str] = None
    is_private: Optional[bool] = None
    wall_closed: Optional[bool] = None
    following_count: int = 0
    posts_count: int = 0
    created_at: PostgresDateTime
    is_following: Optional[bool] = None
    is_followed_by: Optional[bool] = None

class Clan(IterBaseModel):
    avatar: str
    member_count: int