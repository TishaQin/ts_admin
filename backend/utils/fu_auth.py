# backend/utils/fu_auth.py
from typing import Any, Callable, Optional
from ninja.security import HttpBearer
from django.http import HttpRequest
from .fu_exception import AuthenticationError, PermissionDeniedError
from .fu_jwt import decode_token, get_token_from_request


class FuAuth(HttpBearer):
    """认证基类"""

    def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        try:
            payload = decode_token(token)
            request.user_id = payload.get("user_id")
            request.user_roles = payload.get("roles", [])
            return payload
        except Exception as e:
            return None


def require_permissions(permissions: list) -> Callable:
    """权限验证装饰器"""

    def decorator(func: Callable) -> Callable:
        def wrapper(request: HttpRequest, *args, **kwargs):
            if not hasattr(request, "user_roles"):
                token = get_token_from_request(request)
                if not token:
                    raise AuthenticationError("未提供认证令牌")

                try:
                    payload = decode_token(token)
                    request.user_id = payload.get("user_id")
                    request.user_roles = payload.get("roles", [])
                except Exception as e:
                    raise AuthenticationError(f"令牌无效: {str(e)}")

            # 检查权限
            user_permissions = []
            for role in request.user_roles:
                # 这里需要从数据库获取角色对应的权限，简化为示例
                if role == "admin":
                    user_permissions = ["*"]  # 管理员拥有所有权限
                    break

                # 假设从数据库获取的角色权限
                role_permissions = []  # 实际中从数据库加载
                user_permissions.extend(role_permissions)

            if "*" not in user_permissions and not any(
                p in user_permissions for p in permissions
            ):
                raise PermissionDeniedError(
                    f"需要以下权限之一: {', '.join(permissions)}"
                )

            return func(request, *args, **kwargs)

        return wrapper

    return decorator


# 用法示例:
# @require_permissions(["activity:create"])
# def create_activity(request, ...):
#     ...
