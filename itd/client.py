from uuid import UUID
from _io import BufferedReader
from typing import cast

from requests.exceptions import HTTPError

from itd.routes.users import get_user, update_profile, follow, unfollow, get_followers, get_following, update_privacy
from itd.routes.etc import get_top_clans, get_who_to_follow, get_platform_status
from itd.routes.comments import get_comments, add_comment, delete_comment, like_comment, unlike_comment
from itd.routes.hashtags import get_hastags, get_posts_by_hastag
from itd.routes.notifications import get_notifications, mark_as_read, mark_all_as_read, get_unread_notifications_count
from itd.routes.posts import create_post, get_posts, get_post, edit_post, delete_post, pin_post, repost, view_post, get_liked_posts
from itd.routes.reports import report
from itd.routes.search import search
from itd.routes.files import upload_file
from itd.routes.auth import refresh_token, change_password, logout
from itd.routes.verification import verificate, get_verification_status

from itd.models.clan import Clan
from itd.models.user import User, UserProfileUpdate, UserPrivacy, UserFollower, UserWhoToFollow
from itd.models.pagination import Pagination
from itd.models.verification import Verification, VerificationStatus

from itd.request import set_cookies
from itd.exceptions import NoCookie, NoAuthData, SamePassword, InvalidOldPassword, UserNotFound, InvalidProfileData, UserBanned, PendingRequestExists


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
            set_cookies(self.cookies)
            self.refresh_auth()
        else:
            raise NoAuthData()

    def refresh_auth(self) -> str:
        """Обновить access token

        Raises:
            NoCookie: Нет cookie

        Returns:
            str: Токен
        """
        print('refresh token')
        if not self.cookies:
            raise NoCookie()

        res = refresh_token(self.cookies)
        res.raise_for_status()

        self.token = res.json()['accessToken']
        return self.token

    @refresh_on_error
    def change_password(self, old: str, new: str) -> dict:
        """Смена пароля

        Args:
            old (str): Страый пароль
            new (str): Новый пароль

        Raises:
            NoCookie: Нет cookie
            SamePassword: Одинаковые пароли
            InvalidOldPassword: Старый пароль неверный

        Returns:
            dict: Ответ API `{'message': 'Password changed successfully'}`
        """
        if not self.cookies:
            raise NoCookie()

        res = change_password(self.cookies, self.token, old, new)
        if res.json().get('error', {}).get('code') == 'SAME_PASSWORD':
            raise SamePassword()
        if res.json().get('error', {}).get('code') == 'INVALID_OLD_PASSWORD':
            raise InvalidOldPassword()
        res.raise_for_status()

        return res.json()

    @refresh_on_error
    def logout(self) -> dict:
        """Выход из аккаунта

        Raises:
            NoCookie: Нет cookie

        Returns:
            dict: Ответ API
        """
        if not self.cookies:
            raise NoCookie()

        res = logout(self.cookies)
        res.raise_for_status()

        return res.json()

    @refresh_on_error
    def get_user(self, username: str) -> User:
        """Получить пользователя

        Args:
            username (str): username или "me"

        Raises:
            UserNotFound: Пользователь не найден
            UserBanned: Пользователь заблокирован

        Returns:
            User: Пользователь
        """
        res = get_user(self.token, username)
        if res.json().get('error', {}).get('code') == 'NOT_FOUND':
            raise UserNotFound()
        if res.json().get('error', {}).get('code') == 'USER_BLOCKED':
            raise UserBanned()
        res.raise_for_status()

        return User.model_validate(res.json())

    @refresh_on_error
    def get_me(self) -> User:
        """Получить текущего пользователя (me)

        Returns:
            User: Пользователь
        """
        return self.get_user('me')

    @refresh_on_error
    def update_profile(self, username: str | None = None, display_name: str | None = None, bio: str | None = None, banner_id: UUID | None = None) -> UserProfileUpdate:
        """Обновить профиль

        Args:
            username (str | None, optional): username. Defaults to None.
            display_name (str | None, optional): Отображаемое имя. Defaults to None.
            bio (str | None, optional): Биография (о себе). Defaults to None.
            banner_id (UUID | None, optional): UUID баннера. Defaults to None.

        Raises:
            InvalidProfileData: Неправильные данные (валидация не прошла)

        Returns:
            UserProfileUpdate: Обновленный профиль
        """
        res = update_profile(self.token, bio, display_name, username, banner_id)
        if res.status_code == 422 and 'found' in res.json():
            raise InvalidProfileData(*list(res.json()['found'].items())[0])
        res.raise_for_status()

        return UserProfileUpdate.model_validate(res.json())

    @refresh_on_error
    def update_privacy(self, wall_closed: bool = False, private: bool = False) -> UserPrivacy:
        """Обновить настройки приватности

        Args:
            wall_closed (bool, optional): Закрыть стену. Defaults to False.
            private (bool, optional): Приватность. На данный момент неизвестно, что делает этот параметр. Defaults to False.

        Returns:
            UserPrivacy: Обновленные данные приватности
        """
        res = update_privacy(self.token, wall_closed, private)
        res.raise_for_status()

        return UserPrivacy.model_validate(res.json())

    @refresh_on_error
    def follow(self, username: str) -> int:
        """Подписаться на пользователя

        Args:
            username (str): username

        Raises:
            UserNotFound: Пользователь не найден

        Returns:
            int: Число подписчиков после подписки
        """
        res = follow(self.token, username)
        if res.json().get('error', {}).get('code') == 'NOT_FOUND':
            raise UserNotFound()
        res.raise_for_status()

        return res.json()['followersCount']

    @refresh_on_error
    def unfollow(self, username: str) -> int:
        """Отписаться от пользователя

        Args:
            username (str): username

        Raises:
            UserNotFound: Пользователь не найден

        Returns:
            int: Число подписчиков после отписки
        """
        res = unfollow(self.token, username)
        if res.json().get('error', {}).get('code') == 'NOT_FOUND':
            raise UserNotFound()
        res.raise_for_status()

        return res.json()['followersCount']

    @refresh_on_error
    def get_followers(self, username: str, limit: int = 30, page: int = 1) -> tuple[list[UserFollower], Pagination]:
        """Получить подписчиков пользователя

        Args:
            username (str): username
            limit (int, optional): Лимит. Defaults to 30.
            page (int, optional): Страница (при дозагрузке, увеличивайте на 1). Defaults to 1.

        Raises:
            UserNotFound: Пользователь не найден

        Returns:
            list[UserFollower]: Список подписчиков
            Pagination: Данные пагинации (лимит, страница, сколько всего, есть ли еще)
        """
        res = get_followers(self.token, username, limit, page)
        if res.json().get('error', {}).get('code') == 'NOT_FOUND':
            raise UserNotFound()
        res.raise_for_status()

        return [UserFollower.model_validate(user) for user in res.json()['data']['users']], Pagination.model_validate(res.json()['data']['pagination'])

    @refresh_on_error
    def get_following(self, username: str, limit: int = 30, page: int = 1) -> tuple[list[UserFollower], Pagination]:
        """Получить подписки пользователя

        Args:
            username (str): username
            limit (int, optional): Лимит. Defaults to 30.
            page (int, optional): Страница (при дозагрузке, увеличивайте на 1). Defaults to 1.

        Raises:
            UserNotFound: Пользователь не найден

        Returns:
            list[UserFollower]: Список подписок
            Pagination: Данные пагинации (лимит, страница, сколько всего, есть ли еще)
        """
        res = get_following(self.token, username, limit, page)
        if res.json().get('error', {}).get('code') == 'NOT_FOUND':
            raise UserNotFound()
        res.raise_for_status()

        return [UserFollower.model_validate(user) for user in res.json()['data']['users']], Pagination.model_validate(res.json()['data']['pagination'])


    @refresh_on_error
    def verificate(self, file_url: str) -> Verification:
        res = verificate(self.token, file_url)
        if res.json().get('error', {}).get('code') == 'PENDING_REQUEST_EXISTS':
            raise PendingRequestExists()
        res.raise_for_status()

        return Verification.model_validate(res.json())

    @refresh_on_error
    def get_verification_status(self) -> VerificationStatus:
        res = get_verification_status(self.token)
        res.raise_for_status()

        return VerificationStatus.model_validate(res.json())


    @refresh_on_error
    def get_who_to_follow(self) -> list[UserWhoToFollow]:
        res = get_who_to_follow(self.token)
        res.raise_for_status()

        return [UserWhoToFollow.model_validate(user) for user in res.json()['users']]

    @refresh_on_error
    def get_top_clans(self) -> list[Clan]:
        res = get_top_clans(self.token)
        res.raise_for_status()

        return [Clan.model_validate(clan) for clan in res.json()['clans']]

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