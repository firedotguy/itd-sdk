from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class UserPrivacy(BaseModel):
    private: bool | None = Field(None, alias='isPrivate') # none for not me
    wall_closed: bool = Field(False, alias='wallClosed')

    model_config = {'populate_by_name': True}


class UserProfileUpdate(BaseModel):
    id: UUID
    username: str
    display_name: str = Field(alias='displayName')
    bio: str | None = None

    updated_at: datetime | None = Field(None, alias='updatedAt')

    model_config = {'populate_by_name': True}


class UserNotification(BaseModel):
    id: UUID
    username: str
    display_name: str = Field(alias='displayName')
    avatar: str

    model_config = {'populate_by_name': True}


class UserPost(UserNotification):
    verified: bool = False


class UserWhoToFollow(UserPost):
    followers_count: int = Field(0, alias='followersCount')


class UserFollower(UserPost):
    is_following: bool = Field(False, alias='isFollowing') # none for me


class UserSearch(UserFollower, UserWhoToFollow):
    pass


class User(UserSearch, UserPrivacy):
    banner: str | None = None
    bio: str | None = None
    pinned_post_id: UUID | None = Field(None, alias='pinnedPostId')

    following_count: int = Field(0, alias='followingCount')
    posts_count: int = Field(0, alias='postsCount')

    is_followed: bool | None = Field(None, alias='isFollowedBy') # none for me

    created_at: datetime = Field(alias='createdAt')
