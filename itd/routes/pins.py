from itd.request import fetch

def get_pins(token: str):
    return fetch(token, 'get', 'users/me/pins')

def remove_pin(token: str):
    return fetch(token, 'delete', 'users/me/pin')

def set_pin(token: str, slug: str):
    return fetch(token, 'put', 'users/me/pin', {'slug': slug})