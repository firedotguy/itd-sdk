from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from itd.enums import ReportTargetType, ReportReason


class NewReport(BaseModel):
    id: UUID
    created_at: datetime = Field(alias='createdAt')


class Report(NewReport):
    reason: ReportReason
    description: str | None = None

    target_type: ReportTargetType = Field(alias='targetType')
    target_id: UUID
