# core/common/extractor.py
import base64
import jmespath

class Extractor:
    """从响应中提取变量并更新变量上下文"""

    def __init__(self, extractors, variable_ctx):
        self.extractors = extractors or []
        self.variables = variable_ctx

    def extract(self, response_data):
        for item in self.extractors:
            key = item["key"]
            expr = item["expression"]

            # 如果字段是文件类型，跳过提取
            if isinstance(response_data, dict) and key in response_data:
                value = response_data[key]
                if isinstance(value, bytes):  # 如果是文件二进制数据
                    value = base64.b64encode(value).decode('utf-8')  # 转为 base64 编码
                else:
                    value = jmespath.search(expr, response_data)

                self.variables.set(key, value)
