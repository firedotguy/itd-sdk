from iter.request import fetch
from iter.types.responses import SearchResponse, HashtagFeedResponse

def get_hastags(token: str, limit: int = 10) -> SearchResponse:
    return fetch(token, 'get', 'hashtags/trending', {'limit': limit}, response_schema=SearchResponse)

def get_posts_by_hastag(token: str, hashtag: str, limit: int = 20, offset: int = 0) -> HashtagFeedResponse:
    return fetch(token, 'get', f'hashtags/{hashtag}/posts', {'limit': limit, 'offset': offset}, response_schema=HashtagFeedResponse)
