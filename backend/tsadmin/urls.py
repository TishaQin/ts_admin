"""
URL configuration for tsadmin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ninja import NinjaAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

# 创建 API 实例
api = NinjaAPI(
    title="TS Admin API",
    version="1.0.0",
    description="TS Admin API documentation",
)

# 添加 JWT 认证
api.add_router("/token", NinjaJWTDefaultController.router)

# 导入各个应用的 API 路由
from apps.system.api import router as system_router
from apps.business.api import router as business_router

# 注册路由器
api.add_router("/system", system_router)
api.add_router("/business", business_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # Django Ninja API 路由
]

# 开发环境下的媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
