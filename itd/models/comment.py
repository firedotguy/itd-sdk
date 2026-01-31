from pydantic import Field

from itd.models._text import TextObject


class CommentShort(TextObject):
    likes_count: int = Field(0, alias='likesCount')
    replies_count: int = Field(0, alias='repliesCount')
    is_liked: bool = Field(False, alias='isLiked')

    replies: list['CommentShort'] = []