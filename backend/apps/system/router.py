from ninja import Router
from typing import List
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from tsadmin.utils.fu_resp import success
from tsadmin.utils.fu_auth import require_permissions,AuthBearer  # 导入自定义认证类
from tsadmin.utils.fu_jwt import create_access_token

# 在路由初始化时添加认证类
router = Router(tags=["system"]) 
User = get_user_model()  # 动态获取自定义用户模型

@router.post("/users", response={201: dict})
def create_user(request, username: str, password: str):
    """创建新用户"""
    user = User.objects.create(username=username, password=make_password(password))
    return success(data={"id": user.id})


@router.post("/token")
def get_token(request, username: str, password: str):
    """获取用户 Token"""
    user = User.objects.get(username=username)
    if user.check_password(password):
        # 将用户信息作为字典传递给 create_token
        token = create_access_token({"user_id": user.id, "username": user.username}, ["admin"])
        return {"token": token}
    return {"error": "用户名或密码错误"}


@router.get("/")
def list_system_endpoints(request: HttpRequest):
    return {"message": "System API endpoints"}


# 添加认证装饰器
@router.get("/test-auth", response={200: dict})
@require_permissions(["system:test"])
def test_auth(request):
    """测试认证"""
    return success(data={"message": "认证成功"})
