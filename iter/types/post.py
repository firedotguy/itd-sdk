from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from .user import User
from .media import Attachment

class Comment(BaseModel):
    id: str
    content: str
    author: User
    likesCount: int = 0
    repliesCount: int = 0
    isLiked: bool = False
    createdAt: datetime
    attachments: List[Attachment] = []
    replies: List[Comment] = []

class Post(BaseModel):
    id: str
    content: str
    author: User
    attachments: List[Attachment] = []
    likesCount: int = 0
    commentsCount: int = 0
    repostsCount: int = 0
    viewsCount: int = 0
    createdAt: datetime
    isLiked: bool = False
    isReposted: bool = False
    isOwner: bool = False
    isViewed: bool = False
    wallRecipientId: Optional[str] = None
    wallRecipient: Optional[User] = None
    originalPost: Optional[Post] = None
    comments: Optional[List[Comment]] = None

# Rebuild recursive models
Post.model_rebuild()
Comment.model_rebuild()