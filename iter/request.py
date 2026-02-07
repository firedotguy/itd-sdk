import logging, verboselogs
from _io import BufferedReader
from requests import Session, Response, PreparedRequest, Request
from typing import Optional
from pydantic import BaseModel

# Use a named logger for this module
logger = verboselogs.VerboseLogger(__name__)
s = Session()

def dump_res(res: Response):
    return f'Request dump:\n> {res.request.method} {res.request.url}\n> {str(res.request.body) if len(str(res.request.body)) < 1000 else str(res.request.body)[:1000] + '...'}\n> {res.reason} {res.status_code} {res.text if len(res.text) < 1000 else res.text[:1000] + '...'}'
def dump_req(req: PreparedRequest):
    body = str(req.body) if req.body is not None else ""
    return (
        f'Request dump:\n'
        f'> {req.method} {req.url}\n'
        f'> {body if len(body) < 1000 else body[:1000] + "..."}'
    )

def fetch(token: str, method: str, url: str, params: dict = {}, files: dict[str, tuple[str, BufferedReader]] = {}, response_schema: Optional[BaseModel] = None):
    base = f'https://xn--d1ah4a.com/api/{url}'
    headers = {
        "Authorization": f'Bearer {token}',
        "Accept": "application/json",
        "User-Agent": "Iter-Python-Client/1.0"
    }

    req = Request(
        method=method.upper(),
        url=base,
        headers=headers,
        params=params if method.upper() == "GET" else None,
        json=params if method.upper() != "GET" else None,
        files=files
    )
    res = None

    prepared = s.prepare_request(req)

    try:
        res = s.send(
            prepared, 
            timeout=120 if files else 20
        )

        res.raise_for_status()

        if res.ok and response_schema:
            return response_schema.model_validate_json(res.text)
        return res

    except Exception as e:
        logger.error(f'Request failed: {e}')
        raise
    finally:
        dump = dump_req(prepared)
        if res:
            dump = dump_res(res)

        logger.debug(dump)


def set_cookies(cookies: str):
    for cookie in cookies.split('; '):
        s.cookies.set(cookie.split('=')[0], cookie.split('=')[-1], path='/', domain='xn--d1ah4a.com.com')

def auth_fetch(cookies: str | list, method: str, url: str, params: dict = {}, token: str | None = None):
    if isinstance(cookies, list):
        cookies = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
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
