from iter.request import fetch

def create_post(token: str, content: str, wall_recipient_id: int | None = None, attach_ids: list[str] = []):
    data: dict = {'content': content}
    if wall_recipient_id:
        data['wallRecipientId'] = wall_recipient_id
    if attach_ids:
        data['attachmentIds'] = attach_ids

    return fetch(token, 'post', 'posts', data)

def get_posts(token: str, username: str | None = None, limit: int = 20, cursor: int = 0, sort: str = '', tab: str = ''):
    data: dict = {'limit': limit, 'cursor': cursor}
    if username:
        data['username'] = username
    if sort:
        data['sort'] = sort
    if tab:
        data['tab'] = tab

    return fetch(token, 'get', 'posts', data)

def get_post(token: str, id: str):
    return fetch(token, 'get', f'posts/{id}')

def edit_post(token: str, id: str, content: str):
    return fetch(token, 'put', f'posts/{id}', {'content': content})

def delete_post(token: str, id: str):
    return fetch(token, 'delete', f'posts/{id}')

def pin_post(token: str, id: str):
    return fetch(token, 'post', f'posts/{id}/pin')

def repost(token: str, id: str, content: str | None = None):
    data = {}
    if content:
        data['content'] = content
    return fetch(token, 'post', f'posts/{id}/repost', data)

def view_post(token: str, id: str):
    return fetch(token, 'post', f'posts/{id}/view')

def get_liked_posts(token: str, username: str, limit: int = 20, cursor: int = 0):
    return fetch(token, 'get', f'posts/user/{username}/liked', {'limit': limit, 'cursor': cursor})