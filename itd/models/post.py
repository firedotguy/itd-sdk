from pydantic import Field

from itd.models.user import UserPost
from itd.models._text import TextObject


class PostShort(TextObject):
    likes_count: int = Field(0, alias='likesCount')
    comments_count: int = Field(0, alias='commentsCount')
    reposts_count: int = Field(0, alias='repostsCount')
    views_count: int = Field(0, alias='viewsCount')


class OriginalPost(PostShort):
    is_deleted: bool = Field(False, alias='isDeleted')


class Post(PostShort):
    is_liked: bool = Field(False, alias='isLiked')
    is_reposted: bool = Field(False, alias='isReposted')
    is_viewed: bool = Field(False, alias='isViewed')
    is_owner: bool = Field(False, alias='isOwner')

    comments: list = []

    original_post: OriginalPost | None = None

    wall_recipient_id: int | None = None
    wall_recipient: UserPost | None = None
