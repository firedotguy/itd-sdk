from enum import Enum

class NotificationType(Enum):
    WALL_POST = 'wall_post'
    REPLY = 'reply'
    REPOST = 'repost'
    COMMENT = 'comment'
    FOLLOW = 'follow'
    LIKE = 'like'

class NotificationTargetType(Enum):
    POST = 'post'

class ReportTargetType(Enum):
    POST = 'post'
    USER = 'user'
    COMMENT = 'comment'

class ReportTargetReason(Enum):
    SPAM = 'spam' # спам
    VIOLENCE = 'violence' # насилие
    HATE = 'hate' # ненависть
    ADULT = 'adult' # 18+
    FRAUD = 'fraud' # обман\мошенничество
    OTHER = 'other' # другое

class AttachType(Enum):
    AUDIO = 'audio'
    IMAGE = 'image'
    VIDEO = 'video'
    FILE = 'file'

class PostsTab(Enum):
    FOLLOWING = 'following'
    POPULAR = 'popular'
