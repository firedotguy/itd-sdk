from itd.request import fetch

def add_comment(token: str, post_id: str, content: str, reply_comment_id: str | None = None):
    data = {'content': content}
    if reply_comment_id:
        data['replyTo'] = str(reply_comment_id)
    return fetch(token, 'post', f'posts/{post_id}/comments', data)

def get_comments(token: str, post_id: str, limit: int = 20, cursor: int = 0, sort: str = 'popular'):
    return fetch(token, 'get', f'posts/{post_id}/comments', {'limit': limit, 'sort': sort, 'cursor': cursor})

def like_comment(token: str, comment_id: str):
    return fetch(token, 'post', f'comments/{comment_id}/like')

def unlike_comment(token: str, comment_id: str):
    return fetch(token, 'delete', f'comments/{comment_id}/like')

def delete_comment(token: str, comment_id: str):
    return fetch(token, 'delete', f'comments/{comment_id}')
