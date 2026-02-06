from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    id: str
    username: Optional[str] = None
    displayName: str
    avatar: str
    verified: bool = False
    roles: Optional[List[str]] = None
    bio: Optional[str] = None
    followersCount: Optional[int] = 0

class Clan(BaseModel):
    avatar: str
    memberCount: int