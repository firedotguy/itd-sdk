from iter.request import auth_fetch

def refresh_token(cookies: str):
    return auth_fetch(cookies, 'post', 'v1/auth/refresh')['accessToken']

def change_password(cookies: str, token: str, old: str, new: str):
    return auth_fetch(cookies, 'post', 'v1/auth/change-password', {'newPassword': new, 'oldPassword': old}, token)

def logout(cookies: str):
    return auth_fetch(cookies, 'post', 'v1/auth/logout')
