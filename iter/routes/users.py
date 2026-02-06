from iter.request import fetch


def get_user(token: str, username: str):
    return fetch(token, 'get', f'users/{username}')

def update_profile(token: str, bio: str | None = None, display_name: str | None = None, username: str | None = None, banner_id: str | None = None):
    data = {}
    if bio:
        data['bio'] = bio
    if display_name:
        data['displayName'] = display_name
    if username:
        data['username'] = username
    if banner_id:
        data['bannerId'] = banner_id
    return fetch(token, 'put', 'users/me', data)

def update_privacy(token: str, wall_closed: bool = False, private: bool = False):
    data = {}
    if wall_closed:
        data['wallClosed'] = wall_closed
    if private:
        data['isPrivate'] = private
    return fetch(token, 'put', 'users/me/privacy', data)

def follow(token: str, username: str):
    return fetch(token, 'post', f'users/{username}/follow')

def unfollow(token: str, username: str):
    return fetch(token, 'delete', f'users/{username}/follow')

def get_followers(token: str, username: str, limit: int = 30, page: int = 1):
    return fetch(token, 'get', f'users/{username}/followers', {'limit': limit, 'page': page})

def get_following(token: str, username: str, limit: int = 30, page: int = 1):
    return fetch(token, 'get', f'users/{username}/following', {'limit': limit, 'page': page})

