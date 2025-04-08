# core/common/hook_registry.py
class HookTemplateRegistry:
    """前后置脚本模板管理器"""

    def __init__(self):
        self.templates = {}

    def register(self, template: HookTemplate):
        """注册新的模板"""
        self.templates[template.name] = template

    def execute(self, template_name, variable_ctx):
        """执行指定的模板"""
        if template_name not in self.templates:
            raise ValueError(f"模板不存在: {template_name}")

        template = self.templates[template_name]
        executor = HookExecutor([{"type": template.type, "value": template.script}], variable_ctx)
        executor.execute_all()

# 使用 HookTemplateRegistry
hook_registry = HookTemplateRegistry()
