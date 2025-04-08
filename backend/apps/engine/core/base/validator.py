# 抽象断言器
# core/base/validator.py
class BaseValidator:
    def validate(self, response: dict, validation_rules: list) -> bool:
        """
        根据规则验证响应结果
        :param response: 响应数据
        :param validation_rules: 断言规则
        :return: 是否验证通过
        """
        for rule in validation_rules:
            if not self.apply_rule(response, rule):
                return False
        return True

    def apply_rule(self, response: dict, rule: dict) -> bool:
        """
        应用单个规则进行验证
        :param response: 响应数据
        :param rule: 单个验证规则
        :return: 验证结果
        """
        # 基本规则（可以扩展更多类型）
        if rule.get("eq"):
            key, expected_value = rule["eq"]
            return response.get(key) == expected_value
        return False
