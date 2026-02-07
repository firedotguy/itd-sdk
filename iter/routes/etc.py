from iter.request import fetch
from iter.types.responses import ClanListResponse, WhoToFollowResponse, PlatformStatusResponse

def get_top_clans(token: str) -> ClanListResponse:
    return fetch(token, 'get', 'users/stats/top-clans', response_schema=ClanListResponse)

def get_who_to_follow(token: str) -> WhoToFollowResponse:
    return fetch(token, 'get', 'users/suggestions/who-to-follow', response_schema=WhoToFollowResponse)

def get_platform_status(token: str) -> PlatformStatusResponse:
    return fetch(token, 'get', 'platform/status', response_schema=PlatformStatusResponse)