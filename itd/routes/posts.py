from uuid import UUID

from itd.request import fetch
from itd.enums import PostsTab

def create_post(token: str, content: str, wall_recipient_id: UUID | None = None, attach_ids: list[UUID] = []):
    data: dict = {'content': content}
    if wall_recipient_id:
        data['wallRecipientId'] = str(wall_recipient_id)
    if attach_ids:
        data['attachmentIds'] = list(map(str, attach_ids))

    return fetch(token, 'post', 'posts', data)

def get_posts(token: str, cursor: int = 0, tab: PostsTab = PostsTab.POPULAR):
    return fetch(token, 'get', 'posts', {'cursor': cursor, 'tab': tab.value})

def get_post(token: str, id: UUID):
    return fetch(token, 'get', f'posts/{id}')

def edit_post(token: str, id: UUID, content: str):
    return fetch(token, 'put', f'posts/{id}', {'content': content})

def delete_post(token: str, id: UUID):
    return fetch(token, 'delete', f'posts/{id}')

def pin_post(token: str, id: UUID):
    return fetch(token, 'post', f'posts/{id}/pin')

def repost(token: str, id: UUID, content: str | None = None):
    data = {}
    if content:
        data['content'] = content
    return fetch(token, 'post', f'posts/{id}/repost', data)

def view_post(token: str, id: UUID):
    return fetch(token, 'post', f'posts/{id}/view')

def get_liked_posts(token: str, username_or_id: str | UUID, limit: int = 20, cursor: int = 0):
    return fetch(token, 'get', f'posts/user/{username_or_id}/liked', {'limit': limit})

def restore_post(token: str, post_id: UUID):
    return fetch(token, "post", f"posts/{post_id}/restore",)

def like_post(token: str, post_id: UUID):
    return fetch(token, "post", f"posts/{post_id}/like")

def delete_like_post(token: str, post_id: UUID):
    return fetch(token, "delete", f"posts/{post_id}/like")
