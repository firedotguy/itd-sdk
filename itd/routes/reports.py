from itd.request import fetch
from uuid import UUID

def report(token: str, id: UUID, type: str = 'post', reason: str = 'other', description: str = ''):
    return fetch(token, 'post', 'reports', {'targetId': id, 'targetType': type, 'reason': reason, 'description': description})