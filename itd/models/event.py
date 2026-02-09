from uuid import UUID
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from itd.enums import NotificationType, NotificationTargetType
from itd.models.user import UserNotification


class StreamConnect(BaseModel):
    """Событие подключения к SSE потоку"""
    user_id: UUID = Field(alias='userId')
    timestamp: int


class StreamNotification(BaseModel):
    """Уведомление из SSE потока"""
    id: UUID
    type: NotificationType
    
    target_type: NotificationTargetType | None = Field(None, alias='targetType')
    target_id: UUID | None = Field(None, alias='targetId')
    
    preview: str | None = None
    read_at: datetime | None = Field(None, alias='readAt')
    created_at: datetime = Field(alias='createdAt')
    
    user_id: UUID = Field(alias='userId')
    actor: UserNotification
    
    read: bool = False
    sound: bool = True
