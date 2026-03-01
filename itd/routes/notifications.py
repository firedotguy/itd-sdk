from uuid import UUID

from itd.request import fetch, fetch_stream

def get_notifications(token: str, limit: int = 20, offset: int = 0):
    return fetch(token, 'get', 'notifications', {'limit': limit, 'offset': offset})

def mark_as_read(token: str, id: UUID):
    return fetch(token, 'post', f'notifications/{id}/read')

def mark_all_as_read(token: str):
    return fetch(token, 'post', f'notifications/read-all')

def get_unread_notifications_count(token: str):
    return fetch(token, 'get', 'notifications/count')

def stream_notifications(token: str):
    """Получить SSE поток уведомлений

    Returns:
        Response: Streaming response для SSE
    """
    return fetch_stream(token, 'notifications/stream')