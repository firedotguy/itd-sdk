from __future__ import annotations
from _io import BufferedReader
from uuid import UUID
from typing import TYPE_CHECKING

from itd.exceptions import catch_errors
if TYPE_CHECKING:
    from itd.client import Client


@catch_errors()
def upload_file(client: Client, name: str, data: BufferedReader | bytes):
    return client.request('post', 'files/upload', files={'file': (name, data)})

@catch_errors()
def get_file(client: Client, id: UUID):
    return client.request('get', f'files/{id}')

@catch_errors()
def delete_file(client: Client, id: UUID):
    return client.request('delete', f'files/{id}')
