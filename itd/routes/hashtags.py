from warnings import deprecated
from uuid import UUID
from itd.request import fetch

@deprecated("get_hastags устарела используйте get_hashtags")
def get_hastags(token: str, limit: int = 10):
    return fetch(token, 'get', 'hashtags/trending', {'limit': limit})

def get_hashtags(token: str, limit: int = 10):
    return fetch(token, 'get', 'hashtags/trending', {'limit': limit})

@deprecated("get_posts_by_hastag устерла используй get_posts_by_hashtag")
def get_posts_by_hastag(token: str, hashtag: str, limit: int = 20, cursor: UUID | None = None):
    return fetch(token, 'get', f'hashtags/{hashtag}/posts', {'limit': limit, 'cursor': cursor})

def get_posts_by_hashtag(token: str, hashtag: str, limit: int = 20, cursor: UUID | None = None):
    return fetch(token, 'get', f'hashtags/{hashtag}/posts', {'limit': limit, 'cursor': cursor})
