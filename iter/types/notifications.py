from typing import List, Optional
from pydantic import BaseModel

class NotificationActor(BaseModel):
    id: str
    displayName: str
    username: Optional[str] = None
    avatar: str

class Notification(BaseModel):
    id: str
    type: str  # "like", "comment", "follow"
    targetType: str
    targetId: str
    preview: str
    readAt: Optional[str] = None
    createdAt: str
    actor: NotificationActor
    read: bool

class NotificationResponse(BaseModel):
    notifications: List[Notification]
    hasMore: bool