# core/http/requester.py
import httpx
from core.base.requester import BaseRequester

class HTTPRequester(BaseRequester):
    def __init__(self):
        self.client = httpx.Client()

    def send_request(self, request_data: dict) -> dict:
        method = request_data["method"]
        url = request_data["url"]
        headers = request_data.get("headers", {})
        params = request_data.get("params", {})
        data = request_data.get("data", {})

        if method.lower() == "get":
            response = self.client.get(url, params=params, headers=headers)
        elif method.lower() == "post":
            response = self.client.post(url, data=data, headers=headers)
        else:
            raise ValueError("Unsupported HTTP method")
        
        return {"status_code": response.status_code, "body": response.json()}
