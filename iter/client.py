import logging, verboselogs
logger = verboselogs.VerboseLogger(__name__)

import json
import os
from _io import BufferedReader
from typing import cast, Optional

from requests.exceptions import HTTPError

# Import your routes
from iter.routes.users import get_user, update_profile, follow, unfollow, get_followers, get_following, update_privacy
from iter.routes.etc import get_top_clans, get_who_to_follow, get_platform_status
from iter.routes.comments import get_comments, add_comment, delete_comment, like_comment, unlike_comment
from iter.routes.hashtags import get_hastags, get_posts_by_hastag
from iter.routes.notifications import get_notifications, mark_as_read, get_unread_notifications_count
from iter.routes.posts import create_post, get_posts, get_post, edit_post, delete_post, pin_post, repost, view_post, get_liked_posts
from iter.routes.reports import report
from iter.routes.search import search
from iter.routes.files import upload_file
from iter.routes.auth import refresh_token, change_password, logout
from iter.routes.verification import verificate, get_verification_status

from iter.manual_auth import auth

def refresh_on_error(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except HTTPError as e:
            # If Access Token is expired (401)
            if e.response is not None and e.response.status_code == 401:
                logger.notice("Access token expired, attempting refresh")
                self.auth()
                return func(self, *args, **kwargs)
            raise e
    return wrapper


class Client:
    def __init__(self, token: Optional[str] = None, cookies: Optional[str] = None, session_file: Optional[str] = "session.json", email: Optional[str] = None, password: Optional[str] = None, use_manual_login: bool = True):
        self.token = token.replace('Bearer ', '') if token else None
        self.cookies = cookies

        self.manual_login = use_manual_login
        self.session_file = session_file

        self.email = email
        self.password = password

        is_auth = self.auth()
        if not is_auth:
            logger.critical('Cannot login')
            raise RuntimeError('Cannot login')

    def auth(self):
        if (self.session_file 
            and not self.token 
            and not self.cookies):
            self._load_session()

        if (self.manual_login 
            and not self.token 
            and not self.cookies):
            self._manual_login()

        if self.cookies:
            self._refresh_auth()

        return self.token and self.cookies

    def _save_session(self):
        """Saves current credentials to a JSON file."""
        data = {
            "token": self.token,
            "cookies": self.cookies
        }
        with open(self.session_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def _load_session(self):
        """Loads credentials from the session file."""
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.token = data.get("token")
                    self.cookies = data.get("cookies")
            except Exception as e:
                logger.warning(f"Failed to load session file: {e}")

    def _manual_login(self):
        """Triggers the manual authentication flow."""
        if not self.manual_login:
            logger.info('Manual login canceled')
            return False
        logger.info("Starting manual login")
        new_data = auth(self.email, self.password)
        if new_data:
            self.token = new_data.get('token', '').replace('Bearer ', '')
            self.cookies = new_data.get('cookies')
            self._save_session()
            return True
        logger.warning("Manual login failed")

    def refresh_auth(self):
        """Attempts to get a new access token using cookies. Falls back to manual login if cookies expired."""
        if not self.cookies:
            return self._manual_login()

        try:
            logger.info("Refreshing access token")
            self.token = refresh_token(self.cookies).replace('Bearer ', '')
            self._save_session()
            return self.token
        except HTTPError as e:
            if e.response is not None and e.response.status_code in [401, 403]:
                logger.info("Refresh token expired. Manual login required")
                return self._manual_login()
            raise e

    @refresh_on_error
    def logout(self):
        if not self.cookies:
            logger.warning('Cannot logout: no cookies')
            return
        res = logout(self.cookies)
        self.token = None
        self.cookies = None
        if os.path.exists(self.session_file):
            os.remove(self.session_file)
        return res

    @refresh_on_error
    def get_user(self, username: str) -> dict:
        return get_user(self.token, username)

    @refresh_on_error
    def get_me(self) -> dict:
        return self.get_user('me')

    @refresh_on_error
    def update_profile(self, username: str | None = None, display_name: str | None = None, bio: str | None = None, banner_id: str | None = None) -> dict:
        return update_profile(self.token, bio, display_name, username, banner_id)

    @refresh_on_error
    def update_privacy(self, wall_closed: bool = False, private: bool = False):
        return update_privacy(self.token, wall_closed, private)

    @refresh_on_error
    def follow(self, username: str) -> dict:
        return follow(self.token, username)

    @refresh_on_error
    def unfollow(self, username: str) -> dict:
        return unfollow(self.token, username)

    @refresh_on_error
    def get_followers(self, username: str) -> dict:
        return get_followers(self.token, username)

    @refresh_on_error
    def get_following(self, username: str) -> dict:
        return get_following(self.token, username)

    @refresh_on_error
    def add_comment(self, post_id: str, content: str, reply_comment_id: str | None = None):
        return add_comment(self.token, post_id, content, reply_comment_id)

    @refresh_on_error
    def create_post(self, content: str, wall_recipient_id: int | None = None, attach_ids: list[str] = []):
        return create_post(self.token, content, wall_recipient_id, attach_ids)

    @refresh_on_error
    def upload_file(self, name: str, data: BufferedReader):
        return upload_file(self.token, name, data)