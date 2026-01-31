from requests import Response

from itd.request import auth_fetch

def refresh_token(cookies: str) -> Response:
    return auth_fetch(cookies, 'post', 'v1/auth/refresh')

def change_password(cookies: str, token: str, old: str, new: str) -> Response:
    return auth_fetch(cookies, 'post', 'v1/auth/change-password', {'newPassword': new, 'oldPassword': old}, token)

def logout(cookies: str) -> Response:
    return auth_fetch(cookies, 'post', 'v1/auth/logout')
