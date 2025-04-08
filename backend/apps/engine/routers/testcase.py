import logging
from typing import List, Dict, Any, Optional
from ninja import Router, File
from ninja.files import UploadedFile
from typing import List
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from apps.engine.utils.apifox_importer import ApifoxImporter

from ..models import TestSuite, TestCase, TestStep, TestJob, TestReport, TestInterface, ApiInterface
from .schemas import (
    ImportResponse,
    InterfaceSchema,
    CreateInterfaceSchema,
    UpdateInterfaceSchema,
    InterfaceResponseSchema,
    CreateTestSuiteSchema,
    UpdateTestSuiteSchema,
    TestSuiteResponseSchema,
    CreateTestCaseSchema,
    UpdateTestCaseSchema,
    TestCaseResponseSchema,
    CreateTestJobSchema,
    UpdateTestJobSchema,
    TestJobResponseSchema,
    ApiInterfaceSchema,
    ApiInterfaceCreateSchema,
    ApiInterfaceUpdateSchema,
    TestCaseSchema,
    TestCaseCreateSchema,
    TestCaseUpdateSchema,
    TestSuiteSchema,
    TestSuiteCreateSchema,
    TestSuiteUpdateSchema,
)
from tsadmin.utils.fu_auth import require_permissions, AuthBearer
# from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)
# 在路由初始化时添加认证类
router = Router(tags=["engine"], auth=AuthBearer()) # 使用自定义认证类 

# 定义导入接口
@router.post("/import/apifox/file", response=ImportResponse)
def import_apifox_file(request, file: UploadedFile = File(...)):
    """
    通过上传文件导入 Apifox 接口
    """
    try:
        importer = ApifoxImporter()
        
        # 保存上传的文件
        file_path = default_storage.save(f'apifox_imports/{file.name}', ContentFile(file.read()))
        full_path = default_storage.path(file_path)
        
        # 从文件导入
        imported_interfaces = importer.import_from_file(full_path)
        
        # 删除临时文件
        default_storage.delete(file_path)
        
        # 返回导入结果
        return {
            'success': True,
            'message': f'成功导入 {len(imported_interfaces)} 个接口',
            'data': [{
                'id': interface.id,
                'name': interface.name,
                'url': interface.url,
                'method': interface.method
            } for interface in imported_interfaces]
        }
        
    except Exception as e:
        logger.error(f"导入 Apifox 接口时发生错误: {str(e)}")
        return {
            'success': False,
            'message': f'导入失败: {str(e)}'
        }

# 定义 JSON 导入接口
@router.post("/import/apifox/json", response=ImportResponse)
def import_apifox_json(request, data: Dict[str, Any]):
    """
    通过 JSON 数据导入 Apifox 接口
    """
    try:
        importer = ApifoxImporter()
        imported_interfaces = importer.import_from_json(data)
        
        # 返回导入结果
        return {
            'success': True,
            'message': f'成功导入 {len(imported_interfaces)} 个接口',
            'data': [{
                'id': interface.id,
                'name': interface.name,
                'url': interface.url,
                'method': interface.method
            } for interface in imported_interfaces]
        }
        
    except Exception as e:
        logger.error(f"导入 Apifox 接口时发生错误: {str(e)}")
        return {
            'success': False,
            'message': f'导入失败: {str(e)}'
        }
# ==== 单接口 API ====

@router.get("/interface", response=List[InterfaceResponseSchema])
def list_interfaces(request):
    """获取所有单接口"""
    return TestInterface.objects.all()


@router.post("/interface", response=InterfaceResponseSchema)
# @login_required
def create_interface(request, data: CreateInterfaceSchema):
    """创建单接口"""
    api = TestInterface.objects.create(**data.dict())
    return api


@router.get("/interface/{interface_id}", response=InterfaceResponseSchema)
def get_interface(request, interface_id: int):
    """获取单个单接口"""
    return get_object_or_404(TestInterface, id=interface_id)


@router.put("/interface/{interface_id}", response=InterfaceResponseSchema)
def update_interface(request, interface_id: int, data: UpdateInterfaceSchema):
    """更新单接口"""
    api = get_object_or_404(TestInterface, id=interface_id)
    for attr, value in data.dict().items():
        setattr(api, attr, value)
    api.save()
    return api


@router.delete("/interface/{interface_id}")
def delete_interface(request, interface_id: int):
    """删除单接口"""
    api = get_object_or_404(TestInterface, id=interface_id)
    api.delete()
    return {"success": True}


@router.post("/interface/{interface_id}/upload", response=dict)
def upload_file(request, interface_id: int, file: UploadedFile = File(...)):
    """上传文件到单接口"""
    api = get_object_or_404(TestInterface, id=interface_id)
    # 假设文件内容需要存储到接口的 `mock_response` 字段
    api.mock_response = {"file_name": file.name, "file_size": file.size}
    api.save()
    return {"success": True, "file_name": file.name, "file_size": file.size}


@router.post("/interface/{interface_id}/graphql", response=dict)
def execute_graphql_query(request, interface_id: int, query: str):
    """执行 GraphQL 查询"""
    api = get_object_or_404(TestInterface, id=interface_id)
    if api.protocol != "GraphQL":
        return {"error": "该接口不是 GraphQL 类型"}
    # 模拟 GraphQL 查询执行
    response = {"data": {"message": "GraphQL 查询成功", "query": query}}
    return response

# ==== 测试套件 ====
@router.get("/test-suites", response=List[TestSuiteResponseSchema])
def list_test_suites(request):
    return TestSuite.objects.all()


@router.post("/test-suites", response=TestSuiteResponseSchema)
def create_test_suite(request, data: CreateTestSuiteSchema):
    suite = TestSuite.objects.create(**data.dict())
    return suite


@router.get("/test-suites/{suite_id}", response=TestSuiteResponseSchema)
def get_test_suite(request, suite_id: int):
    return get_object_or_404(TestSuite, id=suite_id)


@router.put("/test-suites/{suite_id}", response=TestSuiteResponseSchema)
def update_test_suite(request, suite_id: int, data: UpdateTestSuiteSchema):
    suite = get_object_or_404(TestSuite, id=suite_id)
    for attr, value in data.dict().items():
        setattr(suite, attr, value)
    suite.save()
    return suite


@router.delete("/test-suites/{suite_id}")
def delete_test_suite(request, suite_id: int):
    suite = get_object_or_404(TestSuite, id=suite_id)
    suite.delete()
    return {"success": True}


# ==== 测试用例 ====
@router.get("/test-cases", response=List[TestCaseResponseSchema])
def list_test_cases(request):
    """获取所有测试用例"""
    return TestCase.objects.all()


@router.post("/test-cases", response=TestCaseResponseSchema)
def create_test_case(request, data: CreateTestCaseSchema):
    """创建测试用例"""
    test_case = TestCase.objects.create(**data.dict())
    return test_case


@router.get("/test-cases/{case_id}", response=TestCaseResponseSchema)
def get_test_case(request, case_id: int):
    """获取单个测试用例"""
    return get_object_or_404(TestCase, id=case_id)


@router.put("/test-cases/{case_id}", response=TestCaseResponseSchema)
def update_test_case(request, case_id: int, data: UpdateTestCaseSchema):
    """更新测试用例"""
    test_case = get_object_or_404(TestCase, id=case_id)
    for attr, value in data.dict().items():
        setattr(test_case, attr, value)
    test_case.save()
    return test_case


@router.delete("/test-cases/{case_id}")
def delete_test_case(request, case_id: int):
    """删除测试用例"""
    test_case = get_object_or_404(TestCase, id=case_id)
    test_case.delete()
    return {"success": True}


# ==== 测试任务 ====
@router.get("/test-jobs", response=List[TestJobResponseSchema])
def list_test_jobs(request):
    return TestJob.objects.all()


@router.post("/test-jobs", response=TestJobResponseSchema)
def create_test_job(request, data: CreateTestJobSchema):
    job = TestJob.objects.create(**data.dict())
    return job


@router.get("/test-jobs/{job_id}", response=TestJobResponseSchema)
def get_test_job(request, job_id: int):
    return get_object_or_404(TestJob, id=job_id)


@router.put("/test-jobs/{job_id}", response=TestJobResponseSchema)
def update_test_job(request, job_id: int, data: UpdateTestJobSchema):
    job = get_object_or_404(TestJob, id=job_id)
    for attr, value in data.dict().items():
        setattr(job, attr, value)
    job.save()
    return job


@router.delete("/test-jobs/{job_id}")
def delete_test_job(request, job_id: int):
    job = get_object_or_404(TestJob, id=job_id)
    job.delete()
    return {"success": True}


# ===== ApiInterface 管理 =====
@router.post("/interfaces/", response=ApiInterfaceSchema)
def create_api_interface(request, data: ApiInterfaceCreateSchema):
    """创建接口"""
    interface = ApiInterface.objects.create(**data.dict())
    return interface

@router.get("/interfaces/", response=List[ApiInterfaceSchema])
def list_api_interfaces(request):
    """获取所有接口"""
    return ApiInterface.objects.all()

@router.get("/interfaces/{interface_id}/", response=ApiInterfaceSchema)
def get_api_interface(request, interface_id: int):
    """获取单个接口"""
    return get_object_or_404(ApiInterface, id=interface_id)

@router.put("/interfaces/{interface_id}/", response=ApiInterfaceSchema)
def update_api_interface(request, interface_id: int, data: ApiInterfaceUpdateSchema):
    """更新接口"""
    interface = get_object_or_404(ApiInterface, id=interface_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(interface, key, value)
    interface.save()
    return interface

@router.delete("/interfaces/{interface_id}/")
def delete_api_interface(request, interface_id: int):
    """删除接口"""
    interface = get_object_or_404(ApiInterface, id=interface_id)
    interface.delete()
    return {"success": True}


