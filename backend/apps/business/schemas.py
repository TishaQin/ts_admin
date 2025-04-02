# ✅ Pydantic 数据验证
from typing import List, Optional, Any
from datetime import datetime
from ninja import Schema, ModelSchema
from .models import Activity, ActivityType, ActivityParticipant
from enum import Enum


# 活动状态枚举
class ActivityStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ONGOING = "ongoing"
    ENDED = "ended"
    CANCELED = "canceled"


# 参与者状态枚举
class ParticipantStatus(str, Enum):
    REGISTERED = "registered"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"
    ATTENDED = "attended"


# 可接受参与者的活动状态
ACCEPTABLE_ACTIVITY_STATUS = [ActivityStatus.PUBLISHED, ActivityStatus.ONGOING]

# 作为模型的选项使用的元组列表
ACTIVITY_STATUS_CHOICES = [
    (status.value, status.name.title()) for status in ActivityStatus
]
PARTICIPANT_STATUS_CHOICES = [
    (status.value, status.name.title()) for status in ParticipantStatus
]


# ActivityType 相关 Schema
class ActivityTypeCreate(Schema):
    name: str
    description: Optional[str] = None


class ActivityTypeOut(ModelSchema):
    class Config:
        model = ActivityType
        model_fields = ["id", "name", "description", "created_at", "updated_at"]


# Activity 相关 Schema
class ActivityCreate(Schema):
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    max_participants: int = 0
    activity_type_id: int
    cover_image: Optional[Any] = None
    status: ActivityStatus = ActivityStatus.DRAFT


class ActivityUpdate(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    max_participants: Optional[int] = None
    activity_type_id: Optional[int] = None
    status: Optional[str] = None
    cover_image: Optional[Any] = None


class ActivityOut(ModelSchema):
    activity_type: ActivityTypeOut

    class Config:
        model = Activity
        model_fields = [
            "id",
            "title",
            "description",
            "start_time",
            "end_time",
            "location",
            "max_participants",
            "current_participants",
            "status",
            "cover_image",
            "created_at",
            "updated_at",
            "creator_id",
        ]


# ActivityParticipant 相关 Schema
class ParticipantCreate(Schema):
    activity_id: int
    remark: Optional[str] = None


class ParticipantUpdate(Schema):
    status: str
    remark: Optional[str] = None


class ParticipantOut(ModelSchema):
    class Config:
        model = ActivityParticipant
        model_fields = [
            "id",
            "activity_id",
            "user_id",
            "status",
            "register_time",
            "remark",
        ]


# 错误响应 Schema
class ErrorResponse(Schema):
    message: str


# 分页 Schema
class Pagination(Schema):
    count: int
    page: int
    size: int


class ActivityPagination(Schema):
    pagination: Pagination
    items: List[ActivityOut]
