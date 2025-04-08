# 调度器（同步/异步统一入口）
import asyncio
from .core.base.runner import APIRunner, AsyncAPIRunner

class EngineDispatcher:
    def __init__(self, is_async=False):
        self.is_async = is_async

    def run(self, case_data, **kwargs):
        if self.is_async:
            return asyncio.run(self.run_async(case_data, **kwargs))
        else:
            return self.run_sync(case_data, **kwargs)

    def run_sync(self, case_data, **kwargs):
        runner = APIRunner()
        return runner.run_cases(case_data, **kwargs)

    async def run_async(self, case_data, **kwargs):
        runner = AsyncAPIRunner()
        return await runner.run_cases(case_data, **kwargs)