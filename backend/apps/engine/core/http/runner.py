# HTTP 协议 runner 实现
# core/http/runner.py
from core.base.runner import BaseRunner
from core.http.requester import HTTPRequester

class HTTPRunner(BaseRunner):
    def __init__(self, is_async=False):
        self.is_async = is_async
        self.requester = HTTPRequester()

    def run(self, case: dict, context: dict) -> dict:
        if self.is_async:
            return self.run_async(case, context)
        else:
            return self.run_sync(case, context)

    def run_sync(self, case: dict, context: dict) -> dict:
        response = self.requester.send_request(case["request"])
        # 执行断言
        return response

    async def run_async(self, case: dict, context: dict) -> dict:
        response = await self.requester.send_request(case["request"])
        # 执行断言
        return response
