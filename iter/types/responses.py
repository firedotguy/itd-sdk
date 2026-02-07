from iter.types.user import User, Clan
from iter.types.etc import Hashtag, CursorPagination, PagePagination
from iter.types.post import Post, Comment
from iter.types.notification import Notification
from iter.types.base import IterBaseModel, PostgresDateTime
from typing import List, Optional
from pydantic import Field

# Response models

class PostFeedResponse(IterBaseModel):
    posts: List[Post]
    pagination: CursorPagination

class HashtagFeedResponse(PostFeedResponse):
    hashtag: Hashtag

class UserListResponse(IterBaseModel):
    users: List[User]
    pagination: PagePagination

class SearchResponse(IterBaseModel):
    users: List[User] = Field(default_factory=list)
    hashtags: List[Hashtag] = Field(default_factory=list)

class CommentsResponse(IterBaseModel):
    comments: List[Comment]
    total: int
    has_more: bool
    next_cursor: Optional[int] = None

class WhoToFollowResponse(IterBaseModel):
    users: List[User]

class PostUpdateResponse(IterBaseModel):
    id: str
    content: str
    updated_at: PostgresDateTime

class ReportResponse(IterBaseModel):
    pass # TODO

class VerificateResponse(IterBaseModel):
    pass # TODO

class VerificationStatusResponse(IterBaseModel):
    pass # TODO

# Action and state responses

class LikeResponse(IterBaseModel):
    liked: bool
    likes_count: int

class FollowResponse(IterBaseModel):
    following: bool
    followers_count: int

class StatusResponse(IterBaseModel):
    success: bool = True

class PinResponse(IterBaseModel):
    success: bool
    pinned_post_id: Optional[str] = None

# Account and profile responses

class ProfileUpdateResponse(IterBaseModel):
    id: str
    username: str
    display_name: str
    bio: str
    updated_at: PostgresDateTime

class PrivacyUpdateResponse(IterBaseModel):
    is_private: bool
    wall_closed: bool

# System and notification responses ---

class NotificationListResponse(IterBaseModel):
    notifications: List[Notification]
    has_more: bool

class NotificationCountResponse(IterBaseModel):
    count: int

class PlatformStatusResponse(IterBaseModel):
    read_only: bool

class ClanListResponse(IterBaseModel):
    clans: List[Clan]
    
class SuccessResponse(IterBaseModel):
    success: bool = True