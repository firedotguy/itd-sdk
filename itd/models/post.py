from uuid import UUID

from pydantic import Field, BaseModel

from itd.models.user import UserPost, UserNewPost
from itd.models._text import TextObject
from itd.models.file import PostAttach
from itd.models.comment import Comment


class _PostShort(TextObject):
    likes_count: int = Field(0, alias='likesCount')
    comments_count: int = Field(0, alias='commentsCount')
    reposts_count: int = Field(0, alias='repostsCount')
    views_count: int = Field(0, alias='viewsCount')


class PostShort(_PostShort):
    author: UserPost


class OriginalPost(PostShort):
    is_deleted: bool = Field(False, alias='isDeleted')


class _Post(_PostShort):
    is_liked: bool = Field(False, alias='isLiked')
    is_reposted: bool = Field(False, alias='isReposted')
    is_viewed: bool = Field(False, alias='isViewed')
    is_owner: bool = Field(False, alias='isOwner')

    attachments: list[PostAttach] = []
    comments: list[Comment] = []

    original_post: OriginalPost | None = None

    wall_recipient_id: UUID | None = Field(None, alias='wallRecipientId')
    wall_recipient: UserPost | None = Field(None, alias='wallRecipient')


class Post(_Post, PostShort):
    pass


class NewPost(_Post):
    author: UserNewPost


class LikePostResponse(BaseModel):
    liked: bool
    likes_count: int = Field(alias="likesCount")
