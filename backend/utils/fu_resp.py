# backend/utils/fu_resp.py
from typing import Any, Dict, List, Optional, TypeVar, Generic, Union
from pydantic import BaseModel, Field
from ninja import Schema

T = TypeVar("T")


class ResponseSchema(Schema, Generic[T]):
    """统一响应模式"""

    code: int = 200
    message: str = "成功"
    data: Optional[T] = None


class PaginationSchema(Schema):
    """分页信息"""

    total: int
    page: int
    size: int
    pages: int


class PageResponseSchema(ResponseSchema, Generic[T]):
    """分页响应"""

    pagination: PaginationSchema
    data: List[T] = []


def success(data: Any = None, message: str = "成功") -> Dict[str, Any]:
    """成功响应"""
    return {"code": 200, "message": message, "data": data}


def error(
    code: int = 400, message: str = "请求错误", data: Any = None
) -> Dict[str, Any]:
    """错误响应"""
    return {"code": code, "message": message, "data": data}


def page_success(items: List[Any], total: int, page: int, size: int) -> Dict[str, Any]:
    """分页成功响应"""
    pages = (total + size - 1) // size if size > 0 else 1

    return {
        "code": 200,
        "message": "成功",
        "data": items,
        "pagination": {"total": total, "page": page, "size": size, "pages": pages},
    }


# 在ninja视图中使用:
# @router.get("/items", response=List[ItemSchema])
# def list_items(request):
#     items = Item.objects.all()
#     return success(data=[{"id": item.id, "name": item.name} for item in items])
