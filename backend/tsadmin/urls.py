from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from tsadmin.utils.fu_auth import require_permissions,AuthBearer  # 导入自定义认证类


# 创建 API 实例
api = NinjaExtraAPI(
    version="1.0.0", 
    title="TSAdmin API", 
    description="TSAdmin API 文档",
    openapi_extra={
        "security": [{"Bearer": []}]
    }
)
api.register_controllers(NinjaJWTDefaultController)


# 导入各个应用的 API 路由
try:
    from apps.system.router import router as system_router
    from backend.apps.engine.routers import router as engine_router

    api.add_router("/sys", system_router)
    api.add_router("/engine", engine_router)
except ImportError as e:
    import logging

    logging.error(f"API 路由导入失败: {e}")

# 定义 URL 路由
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # Django Ninja API 路由
]

# 开发环境下的媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
