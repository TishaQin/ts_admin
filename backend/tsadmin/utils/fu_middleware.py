# # backend/utils/fu_middleware.py
# from django.conf import settings
# from django.http import HttpResponseForbidden
# from django.utils.deprecation import MiddlewareMixin
# from ratelimit.decorators import ratelimit
# from ratelimit.exceptions import Ratelimited


# class IPWhitelistMiddleware(MiddlewareMixin):
#     """IP白名单中间件"""

#     def __init__(self, get_response=None):
#         super().__init__(get_response)
#         self.whitelist = settings.IP_WHITELIST

#     def process_request(self, request):
#         ip = request.META.get("REMOTE_ADDR")
#         if ip not in self.whitelist:
#             return HttpResponseForbidden("IP not allowed")
#         return None


# class RateLimitMiddleware(MiddlewareMixin):
#     """请求频率限制中间件"""

#     def process_request(self, request):
#         try:
#             # 使用 ratelimit 装饰器
#             @ratelimit(key="ip", rate=settings.RATELIMIT_RATE)
#             def rate_limited_view(request):
#                 return None

#             return rate_limited_view(request)
#         except Ratelimited:
#             return HttpResponseForbidden("Too many requests. Please try again later.")
