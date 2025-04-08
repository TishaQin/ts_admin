from ninja import Schema, ModelSchema
from typing import Optional, List,datetime
from models import (
    Project, Environment, VariableSet, Database, ApiInterface,
    TestSuite, TestCase, TestStep, TestJob, SchedulePlan,
    CeleryTaskRecord, TestReport, CaseReport, StepReport,
    HookTemplate, CustomAssertion, ExceptionCategory,
    ExceptionRecord, ToolFunction, DataGenerator
)

class ProjectCreateSchema(Schema):
    name: str
    description: Optional[str] = ""

class ProjectUpdateSchema(Schema):
    name: Optional[str]
    description: Optional[str]

class ProjectDetailSchema(ModelSchema):
    class Config:
        model = Project
        model_fields = '__all__'

# ==== Environment ====
class EnvironmentCreateSchema(Schema):
    name: str
    project_id: int
    base_url: str
    variables: Optional[dict] = {}

class EnvironmentUpdateSchema(Schema):
    name: Optional[str]
    base_url: Optional[str]
    variables: Optional[dict]

class EnvironmentDetailSchema(ModelSchema):
    class Config:
        model = Environment
        model_fields = '__all__'

# ==== VariableSet ====
class VariableSetCreateSchema(Schema):
    name: str
    variables: dict
    project_id: int

class VariableSetUpdateSchema(Schema):
    name: Optional[str]
    variables: Optional[dict]

class VariableSetDetailSchema(ModelSchema):
    class Config:
        model = VariableSet
        model_fields = '__all__'

# ==== Database ====
class DatabaseCreateSchema(Schema):
    name: str
    db_type: str
    host: str
    port: int
    username: str
    password: str
    db_name: str
    project_id: int

class DatabaseUpdateSchema(Schema):
    name: Optional[str]
    db_type: Optional[str]
    host: Optional[str]
    port: Optional[int]
    username: Optional[str]
    password: Optional[str]
    db_name: Optional[str]

class DatabaseDetailSchema(ModelSchema):
    class Config:
        model = Database
        model_fields = '__all__'

# ==== ApiInterface ====
class ApiInterfaceCreateSchema(Schema):
    name: str
    project_id: int
    protocol: str
    method: Optional[str] = None
    url: Optional[str] = None
    headers: Optional[dict] = {}
    query_params: Optional[dict] = {}
    body: Optional[dict] = {}
    graphql_query: Optional[str] = None
    timeout: Optional[int] = 30
    is_mock: Optional[bool] = False
    mock_response: Optional[dict] = {}

class ApiInterfaceUpdateSchema(Schema):
    id: int
    name: Optional[str]
    method: Optional[str]
    url: Optional[str]
    headers: Optional[dict]
    query_params: Optional[dict]
    body: Optional[dict]
    graphql_query: Optional[str]
    timeout: Optional[int]
    is_mock: Optional[bool]
    mock_response: Optional[dict]

class ApiInterfaceDetailSchema(ModelSchema):
    class Config:
        model = ApiInterface
        model_fields = '__all__'
        
# ==== TestSuite ====
class TestSuiteCreateSchema(Schema):
    name: str
    project: int
    is_public: bool = False
    parent: Optional[int] = None

class TestSuiteUpdateSchema(TestSuiteCreateSchema):
    pass

class TestSuiteDetailSchema(ModelSchema):
    class Config:
        model = TestSuite
        model_fields = '__all__'
        
# ==== TestCase ====
class TestCaseCreateSchema(Schema):
    name: str
    suite: int
    project: int
    environment: int
    protocol: str
    variable_set: Optional[int] = None
    order: int = 0
    retries: int = 0
    execution_count: int = 1
    skip: bool = False
    version: str = "v1.0"

class TestCaseUpdateSchema(TestCaseCreateSchema):
    pass

class TestCaseDetailSchema(ModelSchema):
    class Config:
        model = TestCase
        model_fields = '__all__'

# ==== TestStep ====
class TestStepCreateSchema(Schema):
    testcase: int
    name: str
    order: int = 0
    action_type: str
    api_interface: Optional[int] = None
    request_config: dict = {}
    extractors: List = []
    validators: List = []
    setup_hooks: List = []
    teardown_hooks: List = []
    retries: int = 0
    skip: bool = False

class TestStepUpdateSchema(TestStepCreateSchema):
    pass

class TestStepDetailSchema(ModelSchema):
    class Config:
        model = TestStep
        model_fields = '__all__'

# ==== TestJob ====
class TestJobCreateSchema(Schema):
    name: str
    suite: Optional[int] = None
    testcases: List[int] = []
    environment: int
    parallel: bool = False
    run_mode: str = "ALL"

class TestJobUpdateSchema(TestJobCreateSchema):
    status: Optional[str] = "PENDING"

class TestJobDetailSchema(ModelSchema):
    class Config:
        model = TestJob
        model_fields = '__all__'

# ==== SchedulePlan ====
class SchedulePlanCreateSchema(Schema):
    name: str
    cron: str
    job: int
    enabled: bool = True

class SchedulePlanUpdateSchema(SchedulePlanCreateSchema):
    pass

class SchedulePlanDetailSchema(ModelSchema):
    class Config:
        model = SchedulePlan
        model_fields = '__all__'

# ==== CeleryTaskRecord ====
class CeleryTaskRecordCreateSchema(Schema):
    job: int
    task_id: str

class CeleryTaskRecordUpdateSchema(Schema):
    status: Optional[str] = "PENDING"
    result: Optional[dict] = {}
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

class CeleryTaskRecordDetailSchema(CeleryTaskRecordCreateSchema, CeleryTaskRecordUpdateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

# ==== TestReport ====
class TestReportCreateSchema(Schema):
    job: int
    report_type: str
    summary: dict
    logs: Optional[str] = ""

class TestReportUpdateSchema(TestReportCreateSchema):
    pass

class TestReportDetailSchema(TestReportCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

# ==== CaseReport ====
class CaseReportCreateSchema(Schema):
    report: int
    testcase: int
    status: str
    duration: float
    extract_result: dict
    validator_result: List = []
    error_message: Optional[str] = None

class CaseReportUpdateSchema(CaseReportCreateSchema):
    pass

class CaseReportDetailSchema(CaseReportCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

# ==== StepReport ====
class StepReportCreateSchema(Schema):
    case_report: int
    step: int
    status: str
    duration: float
    extract_result: dict
    validator_result: List = []
    error_message: Optional[str] = None

class StepReportUpdateSchema(StepReportCreateSchema):
    pass

class StepReportDetailSchema(StepReportCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

# ==== HookTemplate ====
class HookTemplateCreateSchema(Schema):
    name: str
    hook_type: str
    language: str = "PYTHON"
    script: str

class HookTemplateUpdateSchema(HookTemplateCreateSchema):
    pass

class HookTemplateDetailSchema(HookTemplateCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

# ==== CustomAssertion ====
class CustomAssertionCreateSchema(Schema):
    name: str
    script: str

class CustomAssertionUpdateSchema(CustomAssertionCreateSchema):
    pass

class CustomAssertionDetailSchema(CustomAssertionCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

# ==== ExceptionCategory ====
class ExceptionCategoryCreateSchema(Schema):
    name: str

class ExceptionCategoryUpdateSchema(ExceptionCategoryCreateSchema):
    pass

class ExceptionCategoryDetailSchema(ExceptionCategoryCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

# ==== ExceptionRecord ====
class ExceptionRecordCreateSchema(Schema):
    category: Optional[int] = None
    job: int
    detail: str
    source: str

class ExceptionRecordUpdateSchema(ExceptionRecordCreateSchema):
    pass

class ExceptionRecordDetailSchema(ExceptionRecordCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

# ==== ToolFunction ====
class ToolFunctionCreateSchema(Schema):
    name: str
    description: Optional[str] = ""
    script: str
    language: str = "PYTHON"

class ToolFunctionUpdateSchema(ToolFunctionCreateSchema):
    pass

class ToolFunctionDetailSchema(ToolFunctionCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

# ==== DataGenerator ====
class DataGeneratorCreateSchema(Schema):
    name: str
    config: dict = {}
    script: str

class DataGeneratorUpdateSchema(DataGeneratorCreateSchema):
    pass

class DataGeneratorDetailSchema(DataGeneratorCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime
