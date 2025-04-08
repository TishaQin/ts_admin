from threading import local
from django.contrib.auth.models import AnonymousUser

_user = local()

def get_current_user():
    """获取当前请求的用户"""
    user = getattr(_user, "user", None)
    if isinstance(user, AnonymousUser):  # 如果是匿名用户，返回 None
        return None
    return user

class CurrentUserMiddleware:
    """中间件：将当前登录用户注入到线程上下文中"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.user = getattr(request, "user", None)  # 将当前用户存储到线程上下文中
        response = self.get_response(request)
        return response