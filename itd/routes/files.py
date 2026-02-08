from _io import BufferedReader
from uuid import UUID

from itd.request import fetch


def upload_file(token: str, name: str, data: BufferedReader):
    return fetch(token, 'post', 'files/upload', files={'file': (name, data)})

def get_file(token: str, id: UUID):
    return fetch(token, 'get', f'files/{id}')

def delete_file(token: str, id: UUID):
    return fetch(token, 'delete', f'files/{id}')