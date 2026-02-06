from _io import BufferedReader

from iter.request import fetch


def upload_file(token: str, name: str, data: BufferedReader):
    return fetch(token, 'post', 'files/upload', files={'file': (name, data)})