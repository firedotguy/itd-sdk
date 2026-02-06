from typing import List, Optional
from pydantic import BaseModel
from iter.types.user import User

class Attachment(BaseModel):
    id: str
    type: str
    url: str
    thumbnailUrl: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None

class Post(BaseModel):
    id: str
    content: str
    author: User
    attachments: List[Attachment] = []
    likesCount: int = 0
    commentsCount: int = 0
    repostsCount: int = 0
    viewsCount: int = 0
    createdAt: str
    isLiked: bool = False
    isReposted: bool = False
    isOwner: bool = False
    isViewed: bool = False
    wallRecipientId: Optional[str] = None
    originalPost: Optional[Post] = None

Post.model_rebuild()