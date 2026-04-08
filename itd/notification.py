from __future__ import annotations
from typing import TYPE_CHECKING, cast, Iterator
from uuid import UUID
from datetime import datetime
from json import loads
from threading import Thread

from pydantic import Field, BaseModel, field_validator
from sseclient import SSEClient

from itd.base import ITDBaseModel, refresh_wrapper
from itd.client import Client as ITDClient
from itd.enums import NotificationTargetType, NotificationType, All, ALL
from itd.user import User
from itd.routes.notifications import (
    mark_as_read, mark_all_as_read, get_notifications, get_unread_notifications_count,
    stream_notifications
)
if TYPE_CHECKING:
    from itd.client import Client


class Notification(ITDBaseModel):
    _refreshable = False
    _notifications: Notifications | None = None

    id: UUID
    type: NotificationType

    target_type: NotificationTargetType | None = Field(None, alias='targetType') # none - follows, other - NotificationTragetType.POST
    target_id: UUID | None = Field(None, alias='targetId') # none - follows

    preview: str | None = None # follow - none, comment/reply - content, repost - original post content, like - post content, wall_post - wall post content

    is_read: bool = Field(False, alias='read')
    read_at: datetime | None = Field(None, alias='readAt')
    created_at: datetime = Field(alias='createdAt')

    actor: User
    sound: bool = False # for notifications from stream

    def __init__(self, notification: dict, notifications: Notifications | None = None, client: Client | None = None) -> None:
        super().__init__(client)
        self._notifications = notifications

        for name, value in _NotificationValidate.model_validate(notification).__dict__.items():
            setattr(self, name, value)

    def read(self, client: Client | None = None) -> None:
        mark_as_read(client or self.client, self.id)

        if not self.is_read and self._notifications and self._notifications._unread: # check if already read and has notifications and unread loaded
            self._notifications._unread -= 1

        self.is_read = True
        self.read_at = datetime.now()


class _NotificationValidate(BaseModel, Notification):
    @field_validator('actor', mode='plain')
    @classmethod
    def validate_actor(cls, actor: dict):
        return User._from_dict(actor, False)



class Notifications(ITDBaseModel, list[Notification]):
    _refreshable = False
    _unread: int | None = None

    has_more: bool = True
    total: int = 0


    def _fetch(self, client: Client, page: int) -> dict:
        return get_notifications(client, page).json()['data']

    def load(self, count: int | All = 1000, limit: int = 1000, client: Client | None = None) -> 'Notifications':
        if isinstance(count, All):
            ncount = None
        else:
            ncount = count

        left = ncount or limit # if None get [1000] firstly

        while left > 0: # can be !=, but what if something went wrong
            data = get_notifications(client or self.client, min(limit, left), len(self)).json()
            self.has_more = data['hasMore']

            notifications = data['notifications']
            if ncount is None:
                left = self.total - len(self)

            left -= len(notifications)
            self.extend([Notification(notification, self, self.client) for notification in notifications])

            if len(notifications) < limit or not self.has_more:
                break

            print(f'fetched {len(notifications)} left={left} (was {len(self)})')
        return self

    def load_all(self, limit: int = 1000) -> 'Notifications':
        return self.load(ALL, limit)

    def refresh(self, count: int | None = None, limit: int = 1000) -> 'Notifications': # "None" count means already loaded count
        count = count or len(self)
        self.clear()
        return self.load(count, limit)

    def __setattr__(self, name: str, value) -> None:
        if name == '_client':
            for notification in self:
                notification._client = value
        super().__setattr__(name, value)

    @property
    def all(self) -> "Notifications":
        return self.load_all()

    def read_all(self):
        mark_all_as_read(self.client)
        self._unread = 0

    @property
    def unread_count(self):
        if self._unread is None:
            self._unread = get_unread_notifications_count(self.client).json()['count']
        return self._unread

    def stream(self) -> Iterator[Notification]:
        self._stream = stream_notifications(self.client)
        print('start stream')

        for event in SSEClient(cast(Iterator[bytes], self._stream)).events():
            data = loads(event.data)

            if 'userId' in data and 'timestamp' in data and 'type' not in data:
                print('got init message')
                continue # initial message

            notification = Notification(data, self, self.client)
            self.insert(0, notification)

            exec(f'self.on_{notification.type.value}(notification)')

            yield notification

    def stream_bg(self) -> Thread:
        def _stream():
            for _ in self.stream():
                continue

        thread = Thread(target=_stream)
        thread.start()
        return thread

    def stop_stream(self) -> None:
        if getattr(self, '_stream', None) is not None:
            assert self._stream
            self._stream.close()
            self._stream = None


    # redefine this for your needs (eg notifications.on_like = my_function)
    def on_like(self, notification: Notification) -> None:
        pass

    def on_comment(self, notification: Notification) -> None:
        pass

    def on_reply(self, notification: Notification) -> None:
        pass

    def on_repost(self, notification: Notification) -> None:
        pass

    def on_mention(self, notification: Notification) -> None:
        pass

    def on_follow(self, notification: Notification) -> None:
        pass

    def on_follow_request(self, notification: Notification) -> None:
        pass

    def on_follow_accepted(self, notification: Notification) -> None:
        pass

    def on_comment_like(self, notification: Notification) -> None:
        pass

    def on_comment_mention(self, notification: Notification) -> None:
        pass

    def on_wall_post(self, notification: Notification) -> None:
        pass
