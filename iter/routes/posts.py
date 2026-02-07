from iter.request import fetch
from iter.types.post import Post
from iter.types.responses import PostFeedResponse, Post, PostUpdateResponse, PinResponse

def create_post(token: str, content: str, wall_recipient_id: int | None = None, attach_ids: list[str] = []) -> Post:
    data: dict = {'content': content}
    if wall_recipient_id:
        data['wallRecipientId'] = wall_recipient_id
    if attach_ids:
        data['attachmentIds'] = attach_ids

    return fetch(token, 'post', 'posts', data, response_schema=Post)

def get_posts(token: str, username: str | None = None, limit: int = 20, cursor: int = 0, sort: str = '', tab: str = '') -> PostFeedResponse:
    data: dict = {'limit': limit, 'cursor': cursor}
    if username:
        data['username'] = username
    if sort:
        data['sort'] = sort
    if tab:
        data['tab'] = tab

    return fetch(token, 'get', 'posts', data, response_schema=PostFeedResponse)

def get_post(token: str, id: str) -> Post:
    return fetch(token, 'get', f'posts/{id}', response_schema=Post)

def edit_post(token: str, id: str, content: str) -> PostUpdateResponse:
    return fetch(token, 'put', f'posts/{id}', {'content': content}, response_schema=PostUpdateResponse)

def delete_post(token: str, id: str) -> bool:
    res = fetch(token, 'delete', f'posts/{id}')
    return res.ok

def pin_post(token: str, id: str) -> PinResponse:
    return fetch(token, 'post', f'posts/{id}/pin', response_schema=PinResponse)

def repost(token: str, id: str, content: str | None = None) -> Post:
    data = {}
    if content:
        data['content'] = content
    return fetch(token, 'post', f'posts/{id}/repost', data, response_schema=Post)

def view_post(token: str, id: str) -> bool:
    res = fetch(token, 'post', f'posts/{id}/view')
    return res.ok

def get_liked_posts(token: str, username: str, limit: int = 20, cursor: int = 0) -> PostFeedResponse:
    return fetch(token, 'get', f'posts/user/{username}/liked', {'limit': limit, 'cursor': cursor}, response_schema=PostFeedResponse)