from typing import List, Optional
from pydantic import BaseModel, Field
from iter.types.user import User, UserFull, Clan
from iter.types.etc import Hashtag
from iter.types.post import Post
from iter.types.media import Attachment
from iter.types.etc import CursorPagination, PagePagination
from iter.types.notification import Notification

class SearchResults(BaseModel):
    users: List[User] = Field(default_factory=list)
    hashtags: List[Hashtag] = Field(default_factory=list)

class HashtagFeedData(BaseModel):
    hashtag: Hashtag
    posts: List[Post]
    pagination: CursorPagination

class GetPlatformStatus(BaseModel):
    readOnly: bool

class GetTopClans(BaseModel):
    clans: List[Clan]

class GetWhoToFollow(BaseModel):
    users: List[UserFull]

class GetHashtags(BaseModel):
    data: SearchResults

class GetNotificationCount(BaseModel):
    count: int

class GetNotifications(BaseModel):
    notifications: List[Notification]
    hasMore: bool

class SearchResponse(BaseModel):
    data: SearchResults

class HashtagPostsResponse(BaseModel):
    data: HashtagFeedData

class UserFeedResponse(BaseModel):
    data: List[User]
    pagination: PagePagination

class PostFeedResponse(BaseModel):
    data: List[Post]
    pagination: CursorPagination

class FileUploadResponse(Attachment):
    pass

class ActionSuccess(BaseModel):
    success: bool
    pinnedPostId: Optional[str] = None

class LikeResponse(BaseModel):
    liked: bool
    likesCount: int

class FollowResponse(BaseModel):
    following: bool
    followersCount: int