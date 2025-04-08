import logging
from typing import Dict, Any, Optional
from ninja import Router
from django.shortcuts import get_object_or_404
from django.db import transaction
from ..models import TestCase, TestStep, TestReport, CaseReport, StepReport
from ..utils.variable_handler import VariableHandler
from ..utils.sql_executor import SQLExecutor
from ..utils.assertion_handler import AssertionHandler
from ..utils.api_request import APIRequest
from .schemas import (
    TestCaseRunSchema,
    TestCaseRunResponse,
    StepResultSchema,
    CaseResultSchema
)

logger = logging.getLogger(__name__)
router = Router()

class TestCaseRunner:
    def __init__(self, test_case: TestCase, environment_id: int):
        self.test_case = test_case
        self.environment_id = environment_id
        self.variable_handler = VariableHandler()
        self.sql_executor = SQLExecutor()
        self.assertion_handler = AssertionHandler()
        self.api_request = APIRequest()
        self.step_results = []
        self.case_result = None

    def run(self) -> CaseResultSchema:
        """执行测试用例"""
        try:
            # 1. 加载测试用例和相关配置
            self._load_test_case_config()
            
            # 2. 执行前置 SQL 脚本
            self._execute_pre_sql()
            
            # 3. 执行测试步骤
            for step in self.test_case.steps.all().order_by('order'):
                step_result = self._execute_step(step)
                self.step_results.append(step_result)
            
            # 4. 执行后置 SQL 脚本
            self._execute_post_sql()
            
            # 5. 生成测试报告
            self.case_result = self._generate_report()
            
            return self.case_result
            
        except Exception as e:
            logger.error(f"执行测试用例时发生错误: {str(e)}")
            raise

    def _load_test_case_config(self):
        """加载测试用例配置"""
        # 加载环境变量
        self.variable_handler.load_environment_variables(self.environment_id)
        
        # 加载变量集
        if self.test_case.variable_set:
            self.variable_handler.load_variable_set(self.test_case.variable_set.id)
        
        # 加载测试用例变量
        self.variable_handler.load_test_case_variables(self.test_case.id)

    def _execute_pre_sql(self):
        """执行前置 SQL 脚本"""
        if self.test_case.pre_sql:
            self.sql_executor.execute_sql(
                self.test_case.pre_sql,
                self.test_case.database,
                self.variable_handler.get_variables()
            )

    def _execute_step(self, step: TestStep) -> StepResultSchema:
        """执行单个测试步骤"""
        try:
            # 1. 处理变量替换
            processed_request = self.variable_handler.replace_variables(step.request_config)
            
            # 2. 发送 API 请求
            response = self.api_request.send_request(
                step.api_interface,
                processed_request,
                self.variable_handler.get_variables()
            )
            
            # 3. 提取响应数据
            extracted_data = self.variable_handler.extract_data(
                response,
                step.extractors
            )
            
            # 4. 执行断言
            assertion_results = self.assertion_handler.validate(
                response,
                step.validators,
                self.variable_handler.get_variables()
            )
            
            # 5. 记录步骤结果
            return StepResultSchema(
                step_id=step.id,
                status="PASS" if all(r.success for r in assertion_results) else "FAIL",
                request=processed_request,
                response=response,
                extracted_data=extracted_data,
                assertion_results=assertion_results,
                error_message=None
            )
            
        except Exception as e:
            logger.error(f"执行测试步骤时发生错误: {str(e)}")
            return StepResultSchema(
                step_id=step.id,
                status="ERROR",
                request=processed_request,
                response=None,
                extracted_data={},
                assertion_results=[],
                error_message=str(e)
            )

    def _execute_post_sql(self):
        """执行后置 SQL 脚本"""
        if self.test_case.post_sql:
            self.sql_executor.execute_sql(
                self.test_case.post_sql,
                self.test_case.database,
                self.variable_handler.get_variables()
            )

    def _generate_report(self) -> CaseResultSchema:
        """生成测试报告"""
        # 计算用例状态
        step_statuses = [result.status for result in self.step_results]
        case_status = "PASS" if all(status == "PASS" for status in step_statuses) else "FAIL"
        
        # 创建测试报告
        with transaction.atomic():
            # 创建主报告
            report = TestReport.objects.create(
                test_case=self.test_case,
                status=case_status,
                environment_id=self.environment_id
            )
            
            # 创建用例报告
            case_report = CaseReport.objects.create(
                report=report,
                test_case=self.test_case,
                status=case_status
            )
            
            # 创建步骤报告
            for step_result in self.step_results:
                StepReport.objects.create(
                    case_report=case_report,
                    step_id=step_result.step_id,
                    status=step_result.status,
                    request=step_result.request,
                    response=step_result.response,
                    extracted_data=step_result.extracted_data,
                    assertion_results=step_result.assertion_results,
                    error_message=step_result.error_message
                )
        
        return CaseResultSchema(
            case_id=self.test_case.id,
            status=case_status,
            step_results=self.step_results,
            report_id=report.id
        )

@router.post("/test-cases/{case_id}/run", response=TestCaseRunResponse)
def run_test_case(request, case_id: int, data: TestCaseRunSchema):
    """执行测试用例"""
    test_case = get_object_or_404(TestCase, id=case_id)
    runner = TestCaseRunner(test_case, data.environment_id)
    result = runner.run()
    return TestCaseRunResponse(
        success=True,
        message="测试用例执行完成",
        data=result
    )
