import logging, verboselogs
from _io import BufferedReader
from requests import Session, Response
from typing import Optional
from pydantic import BaseModel

# Use a named logger for this module
logger = verboselogs.VerboseLogger(__name__)
s = Session()

def dump_res(res: Response):
    return f'> Req\n> {res.request.method} {res.request.url}\n> {res.request.body}\n\n> Res\n> {res.reason} {res.status_code}\n> {res.text}'

def fetch(token: str, method: str, url: str, params: dict = {}, files: dict[str, tuple[str, BufferedReader]] = {}, response_schema: Optional[BaseModel] = None):
    base = f'https://xn--d1ah4a.com/api/{url}'
    headers = {
        "Authorization": f'Bearer {token}',
        "Accept": "application/json",
        "User-Agent": "Iter-Python-Client/1.0"
    }
    
    method = method.upper()

    try:
        if method == "GET":
            res = s.get(base, timeout=20, params=params, headers=headers)
        else:
            res = s.request(method, base, timeout=120 if files else 20, json=params, headers=headers, files=files)
        
        res.raise_for_status()

        if res.ok and response_schema:
            return response_schema.model_validate(res.json())
        return res

    except Exception as e:
        logger.error(f'Request failed: {e}')
    finally:
        logger.debug(dump_res(res))

def set_cookies(cookies: str):
    for cookie in cookies.split('; '):
        s.cookies.set(cookie.split('=')[0], cookie.split('=')[-1], path='/', domain='xn--d1ah4a.com.com')

def auth_fetch(cookies: str, method: str, url: str, params: dict = {}, token: str | None = None):
    headers = {
        "Host": "xn--d1ah4a.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://xn--d1ah4a.com/",
        "Content-Type": "application/json",
        "Origin": "https://xn--d1ah4a.com",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Cookie": cookies,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=4",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Content-Length": "0",
        "TE": "trailers",
    }
    if token:
        headers['Authorization'] = 'Bearer ' + token

    if method == 'get':
        res = s.get(f'https://xn--d1ah4a.com/api/{url}', timeout=20, params=params, headers=headers)
    else:
        res = s.request(method, f'https://xn--d1ah4a.com/api/{url}', timeout=20, json=params, headers=headers)
    res.raise_for_status()
    return res.json()
