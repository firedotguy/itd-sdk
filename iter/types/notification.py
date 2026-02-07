from typing import Optional, Annotated
from datetime import datetime
from iter.types.base import IterBaseModel, PostgresDateTime

class NotificationActor(IterBaseModel):
    id: str
    displayName: str
    username: Optional[str] = None
    avatar: str

class Notification(IterBaseModel):
    id: str
    type: str # "like", "comment", "follow", "repost"
    targetType: Optional[str] = None
    targetId: Optional[str] = None
    preview: Optional[str] = None
    readAt: Optional[PostgresDateTime] = None
    createdAt: PostgresDateTime
    actor: NotificationActor
    read: bool