from itd.request import fetch

def get_hastags(token: str, limit: int = 10):
    return fetch(token, 'get', 'hashtags/trending', {'limit': limit})

def get_posts_by_hastag(token: str, hashtag: str, limit: int = 20, cursor: int = 0):
    return fetch(token, 'get', f'hashtags/{hashtag}/posts', {'limit': limit, 'cursor': cursor})
