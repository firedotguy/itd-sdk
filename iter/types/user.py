from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: str
    username: Optional[str] = None
    displayName: str
    avatar: str
    verified: bool = False
    followersCount: Optional[int] = 0

class UserFull(User):
    banner: Optional[str] = None
    bio: Optional[str] = None
    pin: Optional[str] = None
    pinnedPostId: Optional[str] = None
    isPrivate: Optional[bool] = None
    wallClosed: Optional[bool] = None
    followingCount: int = 0
    postsCount: int = 0
    createdAt: datetime
    isFollowing: Optional[bool] = None
    isFollowedBy: Optional[bool] = None

class Clan(BaseModel):
    avatar: str
    memberCount: int