from _io import BufferedReader
from typing import cast

from requests.exceptions import HTTPError

from iter.routes.users import get_user, update_profile, follow, unfollow, get_followers, get_following, update_privacy
from iter.routes.etc import get_top_clans, get_who_to_follow, get_platform_status
from iter.routes.comments import get_comments, add_comment, delete_comment, like_comment, unlike_comment
from iter.routes.hashtags import get_hastags, get_posts_by_hastag
from iter.routes.notifications import get_notifications, mark_as_read, mark_all_as_read, get_unread_notifications_count
from iter.routes.posts import create_post, get_posts, get_post, edit_post, delete_post, pin_post, repost, view_post, get_liked_posts
from iter.routes.reports import report
from iter.routes.search import search
from iter.routes.files import upload_file
from iter.routes.auth import refresh_token, change_password, logout
from iter.routes.verification import verificate, get_verification_status


def refresh_on_error(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except HTTPError as e:
            if '401' in str(e):
                self.refresh_auth()
                return func(self, *args, **kwargs)
            raise e
    return wrapper


class Client:
    def __init__(self, token: str | None, cookies: str | None = None):
        self.cookies = cookies

        if token:
            self.token = token.replace('Bearer ', '')
        elif self.cookies:
            self.refresh_auth()
        else:
            raise ValueError('Provide token or cookie')

    def refresh_auth(self):
        if self.cookies:
            self.token = refresh_token(self.cookies)
            return self.token
        else:
            print('no cookies')

    @refresh_on_error
    def change_password(self, old: str, new: str):
        if not self.cookies:
            print('no cookies')
            return
        return change_password(self.cookies, self.token, old, new)

    @refresh_on_error
    def logout(self):
        if not self.cookies:
            print('no cookies')
            return
        return logout(self.cookies)


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
    def verificate(self, file_url: str):
        return verificate(self.token, file_url)

    @refresh_on_error
    def get_verification_status(self):
        return get_verification_status(self.token)


    @refresh_on_error
    def get_who_to_follow(self) -> dict:
        return get_who_to_follow(self.token)

    @refresh_on_error
    def get_top_clans(self) -> dict:
        return get_top_clans(self.token)

    @refresh_on_error
    def get_platform_status(self) -> dict:
        return get_platform_status(self.token)


    @refresh_on_error
    def add_comment(self, post_id: str, content: str, reply_comment_id: str | None = None):
        return add_comment(self.token, post_id, content, reply_comment_id)

    @refresh_on_error
    def get_comments(self, post_id: str, limit: int = 20, cursor: int = 0, sort: str = 'popular'):
        return get_comments(self.token, post_id, limit, cursor, sort)

    @refresh_on_error
    def like_comment(self, id: str):
        return like_comment(self.token, id)

    @refresh_on_error
    def unlike_comment(self, id: str):
        return unlike_comment(self.token, id)

    @refresh_on_error
    def delete_comment(self, id: str):
        return delete_comment(self.token, id)


    @refresh_on_error
    def get_hastags(self, limit: int = 10):
        return get_hastags(self.token, limit)

    @refresh_on_error
    def get_posts_by_hashtag(self, hashtag: str, limit: int = 20, cursor: int = 0):
        return get_posts_by_hastag(self.token, hashtag, limit, cursor)


    @refresh_on_error
    def get_notifications(self, limit: int = 20, cursor: int = 0, type: str | None = None):
        return get_notifications(self.token, limit, cursor, type)

    @refresh_on_error
    def mark_as_read(self, id: str):
        return mark_as_read(self.token, id)

    @refresh_on_error
    def mark_all_as_read(self):
        return mark_all_as_read(self.token)

    @refresh_on_error
    def get_unread_notifications_count(self):
        return get_unread_notifications_count(self.token)


    @refresh_on_error
    def create_post(self, content: str, wall_recipient_id: int | None = None, attach_ids: list[str] = []):
        return create_post(self.token, content, wall_recipient_id, attach_ids)

    @refresh_on_error
    def get_posts(self, username: str | None = None, limit: int = 20, cursor: int = 0, sort: str = '', tab: str = ''):
        return get_posts(self.token, username, limit, cursor, sort, tab)

    @refresh_on_error
    def get_post(self, id: str):
        return get_post(self.token, id)

    @refresh_on_error
    def edit_post(self, id: str, content: str):
        return edit_post(self.token, id, content)

    @refresh_on_error
    def delete_post(self, id: str):
        return delete_post(self.token, id)

    @refresh_on_error
    def pin_post(self, id: str):
        return pin_post(self.token, id)

    @refresh_on_error
    def repost(self, id: str, content: str | None = None):
        return repost(self.token, id, content)

    @refresh_on_error
    def view_post(self, id: str):
        return view_post(self.token, id)

    @refresh_on_error
    def get_liked_posts(self, username: str, limit: int = 20, cursor: int = 0):
        return get_liked_posts(self.token, username, limit, cursor)


    @refresh_on_error
    def report(self, id: str, type: str = 'post', reason: str = 'other', description: str = ''):
        return report(self.token, id, type, reason, description)

    @refresh_on_error
    def report_user(self, id: str, reason: str = 'other', description: str = ''):
        return report(self.token, id, 'user', reason, description)

    @refresh_on_error
    def report_post(self, id: str, reason: str = 'other', description: str = ''):
        return report(self.token, id, 'post', reason, description)

    @refresh_on_error
    def report_comment(self, id: str, reason: str = 'other', description: str = ''):
        return report(self.token, id, 'comment', reason, description)


    @refresh_on_error
    def search(self, query: str, user_limit: int = 5, hashtag_limit: int = 5):
        return search(self.token, query, user_limit, hashtag_limit)

    @refresh_on_error
    def search_user(self, query: str, limit: int = 5):
        return search(self.token, query, limit, 0)

    @refresh_on_error
    def search_hashtag(self, query: str, limit: int = 5):
        return search(self.token, query, 0, limit)


    @refresh_on_error
    def upload_file(self, name: str, data: BufferedReader):
        return upload_file(self.token, name, data)

    def update_banner(self, name: str):
        id = self.upload_file(name, cast(BufferedReader, open(name, 'rb')))['id']
        return self.update_profile(banner_id=id)