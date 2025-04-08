# 内建 + 自定义断言
import operator
import logging
import jmespath

logger = logging.getLogger(__name__)

builtin_operators = {
    "eq": operator.eq,
    "ne": operator.ne,
    "gt": operator.gt,
    "lt": operator.lt,
    "ge": operator.ge,
    "le": operator.le,
    "in": lambda a, b: a in b,
    "not_in": lambda a, b: a not in b,
}

class Validator:
    """断言执行器"""

    def __init__(self, validators, variable_ctx, custom_funcs=None):
        self.validators = validators or []
        self.variables = variable_ctx
        self.custom_funcs = custom_funcs or {}

    def validate(self, response_data):
        for validator in self.validators:
            actual = jmespath.search(validator["actual"], response_data)
            expected = self.variables.resolve(validator["expected"])
            op = validator["operator"]

            if op in builtin_operators:
                assert builtin_operators[op](actual, expected), f"{actual} != {expected}"
            elif op in self.custom_funcs:
                func = self.custom_funcs[op]
                assert func(actual, expected), f"自定义断言失败: {op}({actual}, {expected})"
            else:
                raise ValueError(f"不支持的断言操作: {op}")

# core/common/validator.py
class CustomAssertionExecutor:
    """执行自定义断言"""

    def __init__(self, custom_assertions):
        # 将 CustomAssertion 存储到字典中
        self.custom_assertions = {assertion.name: assertion.script for assertion in custom_assertions}

    def execute(self, assertion_name, actual, expected):
        """动态加载并执行断言"""
        if assertion_name not in self.custom_assertions:
            raise ValueError(f"自定义断言不存在: {assertion_name}")

        # 动态执行脚本
        script = self.custom_assertions[assertion_name]
        # 这里可以添加输入验证逻辑
        if not self.is_safe_script(script):
            raise ValueError("不安全的脚本内容")

        local_vars = {"actual": actual, "expected": expected}
        exec(script, {}, local_vars)

        # 如果脚本执行没有抛出异常，表示断言成功
        return local_vars.get("result", False)

    def is_safe_script(self, script):
        # 这里可以添加安全性检查逻辑
        # 例如，检查是否包含危险函数或操作
        dangerous_terms = ["os.system", "subprocess", "eval"]
        return not any(term in script for term in dangerous_terms)
