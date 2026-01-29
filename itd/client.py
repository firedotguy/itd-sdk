from itd.users import get_user
from itd.comments import get_comments, add_comment, delete_comment, like_comment, unlike_comment
from itd.hashtags import get_hastags, get_posts_by_hastag
from itd.notifications import get_notifications, mark_as_read, mark_all_as_read, get_unread_notifications_count
from itd.posts import create_post, get_posts, get_post, edit_post, delete_post, pin_post, repost, view_post
from itd.reports import report
from itd.search import search


class Client:
    def __init__(self, token: str):
        self.token = token.replace('Bearer ', '')

    def get_user(self, username: str) -> dict:
        return get_user(self.token, username)

    def get_me(self) -> dict:
        return self.get_user('me')


    def add_comment(self, post_id: str, content: str, reply_comment_id: str | None = None):
        return add_comment(self.token, post_id, content, reply_comment_id)

    def get_comments(self, post_id: str, limit: int = 20, cursor: int = 0, sort: str = 'popular'):
        return get_comments(self.token, post_id, limit, cursor, sort)

    def like_comment(self, id: str):
        return like_comment(self.token, id)

    def unlike_comment(self, id: str):
        return unlike_comment(self.token, id)

    def delete_comment(self, id: str):
        return delete_comment(self.token, id)


    def get_hastags(self, limit: int = 10):
        return get_hastags(self.token, limit)

    def get_posts_by_hashtag(self, hashtag: str, limit: int = 20, cursor: int = 0):
        return get_posts_by_hastag(self.token, hashtag, limit, cursor)


    def get_notifications(self, limit: int = 20, cursor: int = 0, type: str | None = None):
        return get_notifications(self.token, limit, cursor, type)

    def mark_as_read(self, id: str):
        return mark_as_read(self.token, id)

    def mark_all_as_read(self):
        return mark_all_as_read(self.token)

    def get_unread_notifications_count(self):
        return get_unread_notifications_count(self.token)


    def create_post(self, content: str, wall_recipient_id: int | None = None, attach_ids: list[str] = []):
        return create_post(self.token, content, wall_recipient_id, attach_ids)

    def get_posts(self, username: str | None = None, limit: int = 20, cursor: int = 0, sort: str = '', tab: str = ''):
        return get_posts(self.token, username, limit, cursor, sort, tab)

    def get_post(self, id: str):
        return get_post(self.token, id)

    def edit_post(self, id: str, content: str):
        return edit_post(self.token, id, content)

    def delete_post(self, id: str):
        return delete_post(self.token, id)

    def pin_post(self, id: str):
        return pin_post(self.token, id)

    def repost(self, id: str, content: str | None = None):
        return repost(self.token, id, content)

    def view_post(self, id: str):
        return view_post(self.token, id)


    def report(self, id: str, type: str = 'post', reason: str = 'other', description: str = ''):
        return report(self.token, id, type, reason, description)

    def report_user(self, id: str, reason: str = 'other', description: str = ''):
        return report(self.token, id, 'user', reason, description)

    def report_post(self, id: str, reason: str = 'other', description: str = ''):
        return report(self.token, id, 'post', reason, description)

    def report_comment(self, id: str, reason: str = 'other', description: str = ''):
        return report(self.token, id, 'comment', reason, description)


    def search(self, query: str, user_limit: int = 5, hashtag_limit: int = 5):
        return search(self.token, query, user_limit, hashtag_limit)

    def search_user(self, query: str, limit: int = 5):
        return search(self.token, query, limit, 0)

    def search_hashtag(self, query: str, limit: int = 5):
        return search(self.token, query, 0, limit)