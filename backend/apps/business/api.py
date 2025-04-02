# backend/apps/business/api.py (简化版)
from ninja import Router, Query
from django.http import HttpRequest
from typing import List, Optional

from .models import Activity, ActivityType, ActivityParticipant
from .schemas import ActivityCreate, ActivityUpdate, ActivityOut, ActivityTypeCreate
from utils.fu_resp import success, page_success
from utils.fu_crud import CRUDBase
from utils.fu_auth import require_permissions
from utils.fu_exception import BusinessError

router = Router(tags=["activity"])

# 创建CRUD对象
activity_crud = CRUDBase(Activity)
activity_type_crud = CRUDBase(ActivityType)


# 活动类型API
@router.post("/types", response={201: dict})
@require_permissions(["activity:type:create"])
def create_activity_type(request, data: ActivityTypeCreate):
    activity_type = activity_type_crud.create(obj_in=data.dict())
    return 201, success(data={"id": activity_type.id})


@router.get("/types", response=dict)
def list_activity_types(request):
    types = activity_type_crud.get_multi()
    return success(data=[{"id": t.id, "name": t.name} for t in types])


# 活动API
@router.post("/", response={201: dict})
@require_permissions(["activity:create"])
def create_activity(request, data: ActivityCreate):
    try:
        # 添加创建者信息
        activity_data = data.dict()
        activity_data["creator_id"] = request.user_id  # 假设fu_auth中间件已设置user_id
        activity = activity_crud.create(obj_in=activity_data)
        return 201, success(data={"id": activity.id})
    except Exception as e:
        raise BusinessError(str(e))


@router.get("/", response=dict)
def list_activities(
    request,
    status: Optional[str] = None,
    type_id: Optional[int] = None,
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):

    filters = {}
    if status:
        filters["status"] = status
    if type_id:
        filters["activity_type_id"] = type_id

    result = activity_crud.filter(
        filters=filters,
        search=search,
        search_fields=["title", "description", "location"],
        page=page,
        page_size=page_size,
    )

    # 格式化响应
    items = [
        {
            "id": item.id,
            "title": item.title,
            "status": item.status,
            "start_time": item.start_time,
            "location": item.location,
            "participants": item.current_participants,
        }
        for item in result["items"]
    ]

    return page_success(
        items=items,
        total=result["total"],
        page=result["page"],
        size=result["page_size"],
    )


@router.get("/{activity_id}", response=dict)
def get_activity(request, activity_id: int):
    activity = activity_crud.get(obj_id=activity_id)
    return success(
        data={
            "id": activity.id,
            "title": activity.title,
            "description": activity.description,
            "start_time": activity.start_time,
            "end_time": activity.end_time,
            "location": activity.location,
            "status": activity.status,
            "current_participants": activity.current_participants,
            "max_participants": activity.max_participants,
            "activity_type": {
                "id": activity.activity_type.id,
                "name": activity.activity_type.name,
            },
        }
    )


@router.put("/{activity_id}", response=dict)
@require_permissions(["activity:update"])
def update_activity(request, activity_id: int, data: ActivityUpdate):
    activity = activity_crud.update(
        obj_id=activity_id, obj_in=data.dict(exclude_unset=True)
    )
    return success(message="更新成功")


@router.delete("/{activity_id}", response=dict)
@require_permissions(["activity:delete"])
def delete_activity(request, activity_id: int):
    activity_crud.delete(obj_id=activity_id)
    return success(message="删除成功")
