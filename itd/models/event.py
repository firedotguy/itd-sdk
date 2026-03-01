from uuid import UUID

from pydantic import BaseModel, Field

from itd.models.notification import Notification


class StreamConnect(BaseModel):
    """Событие подключения к SSE потоку"""
    user_id: UUID = Field(alias='userId')
    timestamp: int


class StreamNotification(Notification):
    """Уведомление из SSE потока"""
    user_id: UUID = Field(alias='userId')
    sound: bool = True
