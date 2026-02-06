from iter.request import fetch

def add_comment(token: str, post_id: str, content: str, attachment_ids: list[str] = []):
    data = {'content': content, "attachmentIds": attachment_ids}
    return fetch(token, 'post', f'posts/{post_id}/comments', data)

def reply_to_comment(token: str, comment_id: str, content: str, attachment_ids: list[str] = []):
    data = {'content': content, "attachmentIds": attachment_ids}
    return fetch(token, 'post', f'comments/{comment_id}/replies', data)

def get_comments(token: str, post_id: str, limit: int = 20, cursor: int = 0, sort: str = 'popular'):
    return fetch(token, 'get', f'posts/{post_id}/comments', {'limit': limit, 'sort': sort, 'cursor': cursor})

def like_comment(token: str, comment_id: str):
    return fetch(token, 'post', f'comments/{comment_id}/like')

def unlike_comment(token: str, comment_id: str):
    return fetch(token, 'delete', f'comments/{comment_id}/like')

def delete_comment(token: str, comment_id: str):
    return fetch(token, 'delete', f'comments/{comment_id}')
