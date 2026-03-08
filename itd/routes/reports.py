from uuid import UUID

from itd.request import fetch
from itd.enums import ReportTargetReason, ReportTargetType

def report(token: str, id: UUID, type: ReportTargetType = ReportTargetType.POST, reason: ReportTargetReason = ReportTargetReason.OTHER, description: str | None = None):
    if description is None:
        description = ''
    return fetch(token, 'post', 'reports', {'targetId': str(id), 'targetType': type.value, 'reason': reason.value, 'description': description})