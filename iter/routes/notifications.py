from iter.request import fetch
from iter.types.responses import NotificationListResponse, NotificationCountResponse, StatusResponse

def get_notifications(token: str, limit: int = 20, offset: int = 0, type: str | None = None) -> NotificationListResponse:
    data = {'limit': str(limit), 'cursor': str(offset)}
    if type:
        data['type'] = type
    return fetch(token, 'get', 'notifications', data, response_schema=NotificationListResponse)

def mark_as_read(token: str, id: str) -> StatusResponse:
    return fetch(token, 'post', f'notifications/{id}/read', response_schema=StatusResponse)

def mark_batch_as_read(token: str, ids: list[str]) -> StatusResponse:
    data = {'ids': ids}
    return fetch(token, 'post', 'notifications/read-batch', data, response_schema=StatusResponse)

def get_unread_notifications_count(token: str) -> NotificationCountResponse:
    return fetch(token, 'get', 'notifications/count', response_schema=NotificationCountResponse)