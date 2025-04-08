from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from tsadmin.utils.fu_currentuser import get_current_user

User = get_user_model()


# ==== 抽象基础类 ====
class BaseModel(models.Model):
    # 默认会自动添加一个 `id` 字段，作为主键
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True, blank=True, related_name="created_%(class)s", on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="updated_%(class)s", on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not self.pk and user:
            self.created_by = user
        if user:
            self.updated_by = user
        super().save(*args, **kwargs)
        
    
# ==== 基础业务结构 ====
class GlobalVariable(BaseModel):
    variables = models.JSONField(default=dict)
    is_overridable = models.BooleanField(default=True)
    
class Project(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    tags = TaggableManager(blank=True)
    variables = models.JSONField(default=dict)

class Environment(BaseModel):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, related_name="environments", on_delete=models.CASCADE)
    base_url = models.URLField()
    variables = models.JSONField(default=dict)

class VariableSet(BaseModel):
    variables = models.JSONField(default=dict)
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Database(BaseModel):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    db_type = models.CharField(max_length=20, choices=[("MYSQL", "MySQL"), ("POSTGRESQL", "PostgreSQL")])
    host = models.CharField(max_length=100)
    port = models.IntegerField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    db_name = models.CharField(max_length=100)

# ==== 单接口配置（支持 Apifox 导入） ====
class ApiInterface(BaseModel):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    protocol = models.CharField(max_length=20, choices=[("HTTP", "HTTP"), ("GRAPHQL", "GraphQL")])
    method = models.CharField(max_length=10, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    headers = models.JSONField(default=dict)
    params = models.JSONField(default=dict)
    body = models.JSONField(default=dict)
    graphql_query = models.TextField(blank=True, null=True)
    timeout = models.IntegerField(default=30)
    response_example = models.JSONField(default=dict)
    is_mock = models.BooleanField(default=False)
    mock_response = models.JSONField(default=dict)

# ==== 多步骤用例 ====
class ActionType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=[("HTTP", "HTTP"), ("UI", "UI"), ("RPC", "RPC"), ("DB", "Database")])

class TestSuite(BaseModel):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

class TestCase(BaseModel):
    name = models.CharField(max_length=200)
    suite = models.ForeignKey(TestSuite, on_delete=models.CASCADE, related_name="cases")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    protocol = models.CharField(max_length=20, choices=[("HTTP", "HTTP"), ("GRAPHQL", "GraphQL"), ("UI", "UI"), ("GRPC", "gRPC"), ("DUBBO", "Dubbo")])
    variable_set = models.ForeignKey(VariableSet, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.PositiveIntegerField(default=0)
    retries = models.PositiveIntegerField(default=0)
    execution_count = models.PositiveIntegerField(default=1)
    skip = models.BooleanField(default=False)
    version = models.CharField(max_length=50, default="v1.0")
    
class TestStep(BaseModel):
    testcase = models.ForeignKey(TestCase, related_name="steps", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    action_type = models.ForeignKey(ActionType, on_delete=models.PROTECT)
    api_interface = models.ForeignKey(ApiInterface, null=True, blank=True, on_delete=models.SET_NULL)
    headers = models.JSONField(default=dict)
    params = models.JSONField(default=dict)
    body = models.JSONField(default=dict)
    graphql_query = models.TextField(blank=True, null=True)
    raw_request_config = models.JSONField(default=dict)
    extractors = models.JSONField(default=list)
    validators = models.JSONField(default=list)
    setup_hooks = models.JSONField(default=list)
    teardown_hooks = models.JSONField(default=list)
    retries = models.PositiveIntegerField(default=0)
    skip = models.BooleanField(default=False)
    trace_id = models.CharField(max_length=100, blank=True, null=True)
    log = models.ForeignKey(TestLog, null=True, blank=True, on_delete=models.SET_NULL)

# ==== Hook & 断言脚本 & SQL 前后置 ====
class HookTemplate(BaseModel):
    name = models.CharField(max_length=100)
    hook_type = models.CharField(max_length=20, choices=[("SETUP", "前置"), ("TEARDOWN", "后置")])
    language = models.CharField(max_length=20, choices=[("SQL", "SQL"), ("PYTHON", "Python")], default="PYTHON")
    script = models.TextField()

class CustomAssertion(BaseModel):
    name = models.CharField(max_length=100)
    script = models.TextField()
    
class StepHook(BaseModel):
    step = models.ForeignKey(TestStep, related_name="hook_scripts", on_delete=models.CASCADE)
    hook_template = models.ForeignKey(HookTemplate, on_delete=models.CASCADE)
    enable = models.BooleanField(default=True)
    position = models.CharField(choices=[("SETUP", "前置"), ("TEARDOWN", "后置")], max_length=10)
    
# ==== 日志系统 ====
class TestLog(BaseModel):
    trace_id = models.CharField(max_length=100, unique=True)
    step = models.ForeignKey(TestStep, null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField()
    loki_url = models.URLField(blank=True, null=True)  # 用于跳转到 Loki 查询页面
    response_file = models.FileField(upload_to='response_files/', null=True, blank=True)
    
# ==== 任务调度 & Celery ====
class TestJob(BaseModel):
    name = models.CharField(max_length=200)
    suite = models.ForeignKey(TestSuite, null=True, blank=True, on_delete=models.SET_NULL)
    testcases = models.ManyToManyField(TestCase, blank=True)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    parallel = models.BooleanField(default=False)
    run_mode = models.CharField(max_length=20, choices=[("ALL", "全量"), ("SELECTED", "指定用例")], default="ALL")
    status = models.CharField(max_length=20, choices=[("PENDING", "待执行"), ("RUNNING", "执行中"), ("SUCCESS", "成功"), ("FAILED", "失败")], default="PENDING")
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    result_summary = models.JSONField()

class SchedulePlan(BaseModel):
    name = models.CharField(max_length=100)
    cron = models.CharField(max_length=100)
    job = models.ForeignKey(TestJob, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

class CeleryTaskRecord(BaseModel):
    job = models.ForeignKey(TestJob, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default="PENDING")
    result = models.JSONField(default=dict, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

# ==== 报告系统 ====
class TestReport(BaseModel):
    job = models.ForeignKey(TestJob, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=20, choices=[("DEBUG", "接口调试"), ("CASE", "用例运行"), ("SUITE", "集成用例"), ("SCHEDULE", "定时轮询")])
    summary = models.JSONField()
    logs = models.TextField(blank=True)
    response_file = models.FileField(upload_to="response_files/", null=True, blank=True)

class CaseReport(BaseModel):
    report = models.ForeignKey(TestReport, related_name="case_reports", on_delete=models.CASCADE)
    testcase = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    duration = models.FloatField()
    extract_result = models.JSONField()
    validator_result = models.JSONField(default=list)
    error_message = models.TextField(blank=True, null=True)

class StepReport(BaseModel):
    case_report = models.ForeignKey(CaseReport, related_name="step_reports", on_delete=models.CASCADE)
    step = models.ForeignKey(TestStep, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    duration = models.FloatField()
    extract_result = models.JSONField()
    validator_result = models.JSONField(default=list)
    error_message = models.TextField(blank=True, null=True)



# ==== 异常记录 ====
class ExceptionCategory(BaseModel):
    name = models.CharField(max_length=100)

class ExceptionRecord(BaseModel):
    category = models.ForeignKey(ExceptionCategory, on_delete=models.SET_NULL, null=True)
    job = models.ForeignKey(TestJob, on_delete=models.CASCADE)
    detail = models.TextField()
    source = models.CharField(max_length=100)

# ==== 通用函数工具集（支持造数、数据清洗等） ====
class ToolFunction(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    script = models.TextField()
    language = models.CharField(max_length=20, choices=[("PYTHON", "Python")], default="PYTHON")

class DataGenerator(BaseModel):
    name = models.CharField(max_length=100)
    config = models.JSONField(default=dict)
    script = models.TextField()

# ==== 集成 Locust 性能测试 ====
class PerformanceScenario(BaseModel):
    name = models.CharField(...)
    locust_script = models.TextField()
    users = models.PositiveIntegerField()
    spawn_rate = models.PositiveIntegerField()
    run_time = models.CharField(max_length=50)
