# backend/utils/fu_crud.py
from typing import Type, TypeVar, List, Optional, Any, Dict, Callable, Union
from django.db import models
from django.db.models import Q
from pydantic import BaseModel
from ninja import Schema
from .fu_exception import NotFoundError, ValidationError
from .fu_resp import success, page_success

ModelType = TypeVar("ModelType", bound=models.Model)
SchemaType = TypeVar("SchemaType", bound=Schema)
CreateSchemaType = TypeVar("CreateSchemaType", bound=Schema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=Schema)


class CRUDBase:
    """基础CRUD操作"""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, obj_id: int) -> ModelType:
        """获取单个对象"""
        obj = self.model.objects.filter(id=obj_id).first()
        if not obj:
            raise NotFoundError(f"{self.model.__name__} with id {obj_id} not found")
        return obj

    def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """获取多个对象"""
        return list(self.model.objects.all()[skip : skip + limit])

    def create(self, *, obj_in: Union[CreateSchemaType, Dict[str, Any]]) -> ModelType:
        """创建对象"""
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.dict(exclude_unset=True)

        try:
            obj = self.model.objects.create(**create_data)
            return obj
        except Exception as e:
            raise ValidationError(f"创建失败: {str(e)}")

    def update(
        self, *, obj_id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """更新对象"""
        obj = self.get(obj_id=obj_id)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(obj, field):
                setattr(obj, field, value)

        try:
            obj.save()
            return obj
        except Exception as e:
            raise ValidationError(f"更新失败: {str(e)}")

    def delete(self, *, obj_id: int) -> ModelType:
        """删除对象"""
        obj = self.get(obj_id=obj_id)
        obj.delete()
        return obj

    def filter(
        self,
        *,
        filters: Dict[str, Any] = None,
        search: str = None,
        search_fields: List[str] = None,
        order_by: str = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """过滤并分页"""
        queryset = self.model.objects.all()

        # 应用过滤条件
        if filters:
            filter_kwargs = {}
            for key, value in filters.items():
                if value is not None:
                    if "__" in key:  # 支持过滤操作符 (如 name__contains)
                        filter_kwargs[key] = value
                    else:
                        filter_kwargs[f"{key}"] = value

            if filter_kwargs:
                queryset = queryset.filter(**filter_kwargs)

        # 应用搜索
        if search and search_fields:
            q_objects = Q()
            for field in search_fields:
                q_objects |= Q(**{f"{field}__icontains": search})
            queryset = queryset.filter(q_objects)

        # 应用排序
        if order_by:
            queryset = queryset.order_by(order_by)

        # 计算总数
        total = queryset.count()

        # 应用分页
        start = (page - 1) * page_size
        end = start + page_size
        items = list(queryset[start:end])

        return {"items": items, "total": total, "page": page, "page_size": page_size}


# 用法示例:
# activity_crud = CRUDBase(Activity)
#
# def create_activity(request, data: ActivityCreate):
#     activity = activity_crud.create(obj_in=data)
#     return success(data=activity)
#
# def get_activity(request, activity_id: int):
#     activity = activity_crud.get(obj_id=activity_id)
#     return success(data=activity)
