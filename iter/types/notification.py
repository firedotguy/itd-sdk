from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class NotificationActor(BaseModel):
    id: str
    displayName: str
    username: Optional[str] = None
    avatar: str

class Notification(BaseModel):
    id: str
    type: str # "like", "comment", "follow", "repost"
    targetType: Optional[str] = None
    targetId: Optional[str] = None
    preview: Optional[str] = None
    readAt: Optional[datetime] = None
    createdAt: datetime
    actor: NotificationActor
    read: bool