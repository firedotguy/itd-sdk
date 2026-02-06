from itd.request import fetch

def report(token: str, id: str, type: str = 'post', reason: str = 'other', description: str = ''):
    return fetch(token, 'post', 'reports', {'targetId': id, 'targetType': type, 'reason': reason, 'description': description})