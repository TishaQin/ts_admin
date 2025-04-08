# backend/utils/fu_logger.py
"""
全局日志记录中间件
"""
import json
import logging
import time
from typing import Dict, Any, Optional

from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .fu_request import RequestUtility
from apps.system.models import ApiLog  # 引用system应用中的ApiLog模型

# 创建专用的日志记录器
api_logger = logging.getLogger("api")


class FuLoggerMiddleware(MiddlewareMixin):
    """全局API日志记录中间件"""

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.enable = getattr(settings, "FU_LOG_ENABLE", True)
        self.methods = getattr(
            settings, "FU_LOG_METHODS", ["GET", "POST", "PUT", "DELETE", "PATCH"]
        )
        self.exclude_paths = getattr(
            settings, "FU_LOG_EXCLUDE_PATHS", ["/api/health", "/api/status"]
        )
        self.log_to_db = getattr(settings, "FU_LOG_TO_DB", False)
        self.request_util = RequestUtility()
        self.start_time = 0

    def should_log_request(self, request: HttpRequest) -> bool:
        """判断是否应该记录此请求"""
        # 检查请求方法
        if self.methods != "ALL" and request.method not in self.methods:
            return False

        # 检查排除的路径
        path = request.path
        if any(path.startswith(exclude) for exclude in self.exclude_paths):
            return False

        # 静态文件和媒体文件不记录
        if path.startswith(("/static/", "/media/")):
            return False

        return True

    def process_request(self, request: HttpRequest) -> None:
        """处理请求"""
        if not self.enable or not self.should_log_request(request):
            return

        # 记录请求开始时间
        self.start_time = time.time()

        # 保存请求信息到请求对象，供后续使用
        request.fu_log_info = {
            "request_ip": self.request_util.get_client_ip(request),
            "request_method": request.method,
            "request_path": request.path,
            "request_body": self.request_util.get_request_data(request),
            "request_time": timezone.now(),
            "user_agent": self.request_util.get_user_agent(request),
        }

        # 获取用户信息
        user = getattr(request, "user", None)
        if user and hasattr(user, "username") and not user.is_anonymous:
            request.fu_log_info["request_username"] = user.username
            request.fu_log_info["user_id"] = user.id

    def process_view(
        self, request: HttpRequest, view_func, view_args, view_kwargs
    ) -> None:
        """处理视图函数"""
        if not self.enable or not hasattr(request, "fu_log_info"):
            return

        # 获取模块信息
        module_name = None
        if hasattr(view_func, "cls"):
            view_cls = view_func.cls
            module_name = getattr(view_cls, "module_name", None)
            if not module_name and hasattr(view_cls, "get_queryset"):
                try:
                    queryset = view_cls.get_queryset()
                    module_name = queryset.model._meta.verbose_name
                except Exception:
                    pass

        # 如果还是没有找到模块名，尝试从API路由映射获取
        if not module_name:
            api_model_map = getattr(settings, "FU_API_MODULE_MAP", {})
            for pattern, name in api_model_map.items():
                if pattern in request.path:
                    module_name = name
                    break

        if module_name:
            request.fu_log_info["request_module"] = module_name

    def process_response(
        self, request: HttpRequest, response: HttpResponse
    ) -> HttpResponse:
        """处理响应"""
        if not self.enable or not hasattr(request, "fu_log_info"):
            return response

        # 计算执行时间
        execution_time = (time.time() - self.start_time) * 1000  # 毫秒

        # 尝试解析响应内容
        response_body = None
        response_code = response.status_code
        success = 200 <= response.status_code < 300

        if hasattr(response, "data"):
            # DRF 或 Django Ninja 响应
            response_body = response.data
            if isinstance(response_body, dict) and "code" in response_body:
                response_code = response_body.get("code", response.status_code)
                success = response_code in [200, 2000]
        elif isinstance(response, JsonResponse):
            # 普通JSON响应
            try:
                response_body = json.loads(response.content.decode("utf-8"))
                if isinstance(response_body, dict) and "code" in response_body:
                    response_code = response_body.get("code", response.status_code)
                    success = response_code in [200, 2000]
            except Exception:
                pass

        # 完善日志信息
        log_info = request.fu_log_info
        log_info.update(
            {
                "execution_time": execution_time,
                "response_code": response_code,
                "response_body": response_body,
                "success": success,
                "request_os": log_info["user_agent"]["os"],
                "request_browser": log_info["user_agent"]["browser"],
            }
        )

        # 记录日志
        self._log_request(log_info)

        return response

    def _log_request(self, log_info: Dict[str, Any]) -> Optional[ApiLog]:
        """记录请求日志"""
        # 日志格式化
        log_message = (
            f"[{log_info.get('request_method')}] {log_info.get('request_path')} "
            f"- IP: {log_info.get('request_ip')} "
            f"- User: {log_info.get('request_username', 'Anonymous')} "
            f"- Status: {log_info.get('response_code')} "
            f"- Time: {log_info.get('execution_time'):.2f}ms"
        )

        # 记录到日志文件
        if log_info.get("success", True):
            api_logger.info(log_message, extra=log_info)
        else:
            api_logger.warning(log_message, extra=log_info)

        # 记录到数据库
        if self.log_to_db:
            try:
                return ApiLog.objects.create(
                    request_username=log_info.get("request_username"),
                    request_ip=log_info.get("request_ip"),
                    request_method=log_info.get("request_method"),
                    request_path=log_info.get("request_path"),
                    request_body=log_info.get("request_body"),
                    request_time=log_info.get("request_time"),
                    response_code=log_info.get("response_code"),
                    response_body=log_info.get("response_body"),
                    execution_time=log_info.get("execution_time"),
                    request_os=log_info.get("request_os"),
                    request_browser=log_info.get("request_browser"),
                    request_module=log_info.get("request_module"),
                    success=log_info.get("success", True),
                )
            except Exception as e:
                api_logger.error(f"Failed to save log to database: {str(e)}")

        return None
