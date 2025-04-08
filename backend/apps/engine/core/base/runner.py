# 抽象请求器
# core/base/runner.py
from abc import ABC, abstractmethod

class BaseRunner(ABC):
    @abstractmethod
    def run(self, case: dict, context: dict) -> dict:
        """
        执行单个测试用例
        :param case: 用例数据
        :param context: 执行上下文
        :return: 测试结果
        """
        pass
