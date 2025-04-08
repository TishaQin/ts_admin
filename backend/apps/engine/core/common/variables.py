class VariableContext:
    """管理变量作用域：环境变量 + 用例变量 + 提取变量"""

    def __init__(self, global_vars=None, env_vars=None, case_vars=None, step_vars=None):
        self.context = {}
        self.context.update(global_vars or {})
        self.context.update(env_vars or {})
        self.context.update(case_vars or {})
        self.context.update(step_vars or {})

    def set(self, key, value):
        self.context[key] = value

    def get(self, key, default=None):
        return self.context.get(key, default)

    def merge(self, new_vars: dict):
        self.context.update(new_vars)

    def resolve(self, data):
        """支持 ${var} 格式变量替换"""
        if isinstance(data, str):
            for k, v in self.context.items():
                data = data.replace(f"${{{k}}}", str(v))
            return data
        elif isinstance(data, dict):
            return {k: self.resolve(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.resolve(i) for i in data]
        return data

    def resolve_with_check(self, data):
        """带检查的变量解析"""
        if isinstance(data, str):
            for k, v in self.context.items():
                if f"${{{k}}}" in data:
                    data = data.replace(f"${{{k}}}", str(v))
            return data
        elif isinstance(data, dict):
            return {k: self.resolve_with_check(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.resolve_with_check(i) for i in data]
        return data
