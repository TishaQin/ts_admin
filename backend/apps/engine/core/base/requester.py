# 统一 Runner 接口定义
# core/base/requester.py
from abc import ABC, abstractmethod

class BaseRequester(ABC):
    @abstractmethod
    def send_request(self, request_data: dict) -> dict:
        """
        发送请求的接口
        :param request_data: 请求数据
        :return: 响应结果
        """
        pass
