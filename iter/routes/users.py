from iter.request import fetch
from iter.types.user import UserFull
from iter.types.responses import ProfileUpdateResponse, PrivacyUpdateResponse, FollowResponse, UserListResponse


def get_user(token: str, username: str) -> UserFull:
    return fetch(token, 'get', f'users/{username}', response_schema=UserFull)

def update_profile(token: str, bio: str | None = None, display_name: str | None = None, username: str | None = None, banner_id: str | None = None) -> ProfileUpdateResponse:
    data = {}
    if bio:
        data['bio'] = bio
    if display_name:
        data['displayName'] = display_name
    if username:
        data['username'] = username
    if banner_id:
        data['bannerId'] = banner_id
    return fetch(token, 'put', 'users/me', data, response_schema=ProfileUpdateResponse)

def update_privacy(token: str, wall_closed: bool = False, private: bool = False) -> PrivacyUpdateResponse:
    data = {}
    if wall_closed:
        data['wallClosed'] = wall_closed
    if private:
        data['isPrivate'] = private
    return fetch(token, 'put', 'users/me/privacy', data, response_schema=PrivacyUpdateResponse)

def follow(token: str, username: str) -> FollowResponse:
    return fetch(token, 'post', f'users/{username}/follow', response_schema=FollowResponse)

def unfollow(token: str, username: str) -> FollowResponse:
    return fetch(token, 'delete', f'users/{username}/follow', response_schema=FollowResponse)

def get_followers(token: str, username: str, limit: int = 30, page: int = 1) -> UserListResponse:
    return fetch(token, 'get', f'users/{username}/followers', {'limit': limit, 'page': page}, response_schema=UserListResponse)

def get_following(token: str, username: str, limit: int = 30, page: int = 1) -> UserListResponse:
    return fetch(token, 'get', f'users/{username}/following', {'limit': limit, 'page': page}, response_schema=UserListResponse)

