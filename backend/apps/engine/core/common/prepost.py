# core/common/prepost.py
from core.common.db_executor import execute_sql

class HookExecutor:
    """执行前后置操作"""

    def __init__(self, hooks, variable_ctx):
        self.hooks = hooks
        self.variables = variable_ctx

    def execute_all(self):
        """执行所有前后置操作"""
        for hook in self.hooks:
            if hook["type"] == "SETUP":
                self.execute_setup(hook["value"])
            elif hook["type"] == "TEARDOWN":
                self.execute_teardown(hook["value"])

    def execute_setup(self, script):
        """执行前置脚本"""
        if script.startswith("SQL:"):
            sql = script[4:]
            execute_sql(sql)

    def execute_teardown(self, script):
        """执行后置脚本"""
        if script.startswith("SQL:"):
            sql = script[4:]
            execute_sql(sql)
