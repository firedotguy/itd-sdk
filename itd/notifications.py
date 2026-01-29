from itd.request import fetch

def get_notifications(token: str, limit: int = 20, cursor: int = 0, type: str | None = None):
    data = {'limit': str(limit), 'cursor': str(cursor)}
    if type:
        data['type'] = type
    return fetch(token, 'get', 'notifications', data)

def mark_as_read(token: str, id: str):
    return fetch(token, 'post', f'notification/{id}/read')

def mark_all_as_read(token: str):
    return fetch(token, 'post', f'notification/read-all')

def get_unread_notifications_count(token: str):
    return fetch(token, 'get', 'notifications/count')