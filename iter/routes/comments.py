from iter.request import fetch
from typing import Optional
from iter.types.post import Comment
from iter.types.responses import CommentsResponse, LikeResponse

def add_comment(token: str, post_id: str, content: str, attachment_ids: Optional[list[str]] = None) -> Comment:
    data = {'content': content}
    if attachment_ids:
        data['attachmentIds'] = attachment_ids
    return fetch(token, 'post', f'posts/{post_id}/comments', data, response_schema=Comment)

def reply_to_comment(token: str, comment_id: str, content: str, attachment_ids: Optional[list[str]]  = None) -> Comment:
    data = {'content': content}
    if attachment_ids:
        data['attachmentIds'] = attachment_ids
    return fetch(token, 'post', f'comments/{comment_id}/replies', data, response_schema=Comment)

def get_comments(token: str, post_id: str, limit: int = 20, cursor: int = 0, sort: str = 'popular') -> CommentsResponse:
    return fetch(token, 'get', f'posts/{post_id}/comments', {'limit': limit, 'sort': sort, 'cursor': cursor}, response_schema=CommentsResponse)

def like_comment(token: str, comment_id: str) -> LikeResponse:
    return fetch(token, 'post', f'comments/{comment_id}/like', response_schema=LikeResponse)

def unlike_comment(token: str, comment_id: str) -> LikeResponse:
    return fetch(token, 'delete', f'comments/{comment_id}/like', response_schema=LikeResponse)

def delete_comment(token: str, comment_id: str) -> bool:
    res = fetch(token, 'delete', f'comments/{comment_id}')
    return res.ok
