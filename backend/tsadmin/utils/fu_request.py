import json
import logging
import time
from typing import Dict, Any, Optional
from django.http import HttpRequest, HttpResponse, JsonResponse


class RequestUtility:
    """请求工具类"""

    @staticmethod
    def get_client_ip(request: HttpRequest) -> str:
        """获取客户端IP"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")

    @staticmethod
    def get_user_agent(request: HttpRequest) -> Dict[str, str]:
        """获取用户代理信息"""
        ua = request.META.get("HTTP_USER_AGENT", "")
        # 简单的解析，实际项目中可以使用第三方库如 user-agents
        browser = "Unknown"
        os = "Unknown"

        # 操作系统检测
        if "Windows" in ua:
            os = "Windows"
        elif "Mac" in ua:
            os = "MacOS"
        elif "Linux" in ua:
            os = "Linux"
        elif "Android" in ua:
            os = "Android"
        elif "iOS" in ua or "iPhone" in ua or "iPad" in ua:
            os = "iOS"

        # 浏览器检测
        if "Chrome" in ua and "Safari" in ua:
            browser = "Chrome"
        elif "Firefox" in ua:
            browser = "Firefox"
        elif "Safari" in ua:
            browser = "Safari"
        elif "Edge" in ua:
            browser = "Edge"
        elif "MSIE" in ua or "Trident" in ua:
            browser = "IE"

        return {"browser": browser, "os": os, "user_agent": ua}

    @staticmethod
    def get_request_data(request: HttpRequest) -> Dict[str, Any]:
        """获取请求数据"""
        data = {}

        # GET 参数
        if request.GET:
            data.update(dict(request.GET))

        # POST 参数
        if request.method == "POST":
            if request.content_type and "application/json" in request.content_type:
                try:
                    json_data = json.loads(request.body.decode("utf-8"))
                    if isinstance(json_data, dict):
                        data.update(json_data)
                except Exception:
                    pass
            else:
                data.update(dict(request.POST))

        # 文件
        if request.FILES:
            files = {}
            for key, value in request.FILES.items():
                files[key] = value.name
            data["files"] = files

        # 敏感数据处理
        RequestUtility._mask_sensitive_data(data)

        return data

    @staticmethod
    def _mask_sensitive_data(data: Dict[str, Any]) -> None:
        """掩盖敏感数据"""
        sensitive_fields = [
            "password",
            "token",
            "secret",
            "key",
            "auth",
            "pwd",
            "credential",
        ]

        def _mask_dict(d):
            for key in list(d.keys()):
                if isinstance(d[key], dict):
                    _mask_dict(d[key])
                elif isinstance(d[key], str):
                    for field in sensitive_fields:
                        if field.lower() in key.lower():
                            d[key] = "******"

        if isinstance(data, dict):
            _mask_dict(data)
