# backend/utils/exceptions.py
from ninja.errors import HttpError


class FuException(Exception):
    """基础异常类"""

    status_code = 400
    detail = "错误"

    def __init__(self, detail=None, status_code=None):
        self.detail = detail or self.detail
        self.status_code = status_code or self.status_code
        super().__init__(self.detail)

    def to_http(self):
        """转换为HTTP异常"""
        return HttpError(self.status_code, {"message": self.detail})


# 认证相关异常
class AuthenticationError(FuException):
    status_code = 401
    detail = "认证失败"


class PermissionDeniedError(FuException):
    status_code = 403
    detail = "权限不足"


# 资源相关异常
class NotFoundError(FuException):
    status_code = 404
    detail = "资源不存在"


class ConflictError(FuException):
    status_code = 409
    detail = "资源冲突"


# 业务相关异常
class BusinessError(FuException):
    status_code = 400
    detail = "业务处理错误"


class ValidationError(FuException):
    status_code = 422
    detail = "数据验证失败"


# 系统异常
class SystemError(FuException):
    status_code = 500
    detail = "系统内部错误"


# 为每个业务模块定义特定异常
class ActivityError(BusinessError):
    """活动相关异常"""

    detail = "活动处理错误"


class UserError(BusinessError):
    """用户相关异常"""

    detail = "用户处理错误"
