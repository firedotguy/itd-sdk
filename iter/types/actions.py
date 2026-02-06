from typing import Optional
from pydantic import BaseModel

class LikeResponse(BaseModel):
    liked: bool
    likesCount: int

class FollowResponse(BaseModel):
    following: bool
    followersCount: int

class ProfileUpdateResponse(BaseModel):
    id: str
    username: str
    displayName: str
    bio: Optional[str] = None
    updatedAt: str