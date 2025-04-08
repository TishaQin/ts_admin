from django.urls import reverse
from ninja import NinjaAPI
from ninja.testing import TestClient
from .models import TestInterface, TestSuite, TestCase, TestJob
from .schemas import CreateInterfaceSchema, CreateTestSuiteSchema, CreateTestCaseSchema, CreateTestJobSchema

# 创建 Ninja API 实例
api = NinjaAPI()

class APITests(TestClient):

    def setUp(self):
        # 创建测试数据
        self.test_interface_data = {
            "name": "Test Interface",
            "protocol": "HTTP",
            "method": "GET",
            "url": "https://uppapi.bbxlk.cc/api/payees/template?payment_channel=WF&currency=GBP&region=GB",
            "headers": {"Content-Type": "application/json"},
            "body": {},
            "query_params": {},
            "timeout": 30,
            "is_mock": False,
            "mock_response": {}
        }
        self.test_suite_data = {
            "name": "Test Suite",
            "tags": ["tag1", "tag2"],
            "is_public": True,
            "parent": None
        }
        self.test_case_data = {
            "name": "Test Case",
            "suite": 1,  # 假设 suite ID 为 1
            "api": None,
            "protocol": "HTTP",
            "request_config": {},
            "variables": {},
            "extractors": [],
            "validators": [],
            "setup_hooks": [],
            "teardown_hooks": [],
            "order": 1,
            "retries": 0,
            "version": "1.0"
        }
        self.test_job_data = {
            "name": "Test Job",
            "suite": None,
            "testcases": [],
            "environment": 1,  # 假设环境 ID 为 1
            "parallel": False,
            "run_type": "manual"
        }

    def test_create_interface(self):
        response = self.client.post(reverse('create_interface'), json=self.test_interface_data)
        self.assertEqual(response.status_code, 201)  # 201 Created
        self.assertEqual(response.json()['name'], self.test_interface_data['name'])

    def test_list_interfaces(self):
        TestInterface.objects.create(**self.test_interface_data)
        response = self.client.get(reverse('list_interfaces'))
        self.assertEqual(response.status_code, 200)  # 200 OK
        self.assertEqual(len(response.json()), 1)

    def test_get_interface(self):
        interface = TestInterface.objects.create(**self.test_interface_data)
        response = self.client.get(reverse('get_interface', args=[interface.id]))
        self.assertEqual(response.status_code, 200)  # 200 OK
        self.assertEqual(response.json()['id'], interface.id)

    def test_update_interface(self):
        interface = TestInterface.objects.create(**self.test_interface_data)
        updated_data = {"name": "Updated Interface"}
        response = self.client.put(reverse('update_interface', args=[interface.id]), json=updated_data)
        self.assertEqual(response.status_code, 200)  # 200 OK
        self.assertEqual(response.json()['name'], updated_data['name'])

    def test_delete_interface(self):
        interface = TestInterface.objects.create(**self.test_interface_data)
        response = self.client.delete(reverse('delete_interface', args=[interface.id]))
        self.assertEqual(response.status_code, 204)  # 204 No Content

    def test_create_test_suite(self):
        response = self.client.post(reverse('create_test_suite'), json=self.test_suite_data)
        self.assertEqual(response.status_code, 201)  # 201 Created
        self.assertEqual(response.json()['name'], self.test_suite_data['name'])

    def test_list_test_suites(self):
        TestSuite.objects.create(**self.test_suite_data)
        response = self.client.get(reverse('list_test_suites'))
        self.assertEqual(response.status_code, 200)  # 200 OK
        self.assertEqual(len(response.json()), 1)

    def test_get_test_suite(self):
        suite = TestSuite.objects.create(**self.test_suite_data)
        response = self.client.get(reverse('get_test_suite', args=[suite.id]))
        self.assertEqual(response.status_code, 200)  # 200 OK
        self.assertEqual(response.json()['id'], suite.id)

    def test_update_test_suite(self):
        suite = TestSuite.objects.create(**self.test_suite_data)
        updated_data = {"name": "Updated Suite"}
        response = self.client.put(reverse('update_test_suite', args=[suite.id]), json=updated_data)
        self.assertEqual(response.status_code, 200)  # 200 OK
        self.assertEqual(response.json()['name'], updated_data['name'])

    def test_delete_test_suite(self):
        suite = TestSuite.objects.create(**self.test_suite_data)
        response = self.client.delete(reverse('delete_test_suite', args=[suite.id]))
        self.assertEqual(response.status_code, 204)  # 204 No Content

    def test_create_test_case(self):
        suite = TestSuite.objects.create(**self.test_suite_data)
        self.test_case_data['suite'] = suite.id
        response = self.client.post(reverse('create_test_case'), json=self.test_case_data)
        self.assertEqual(response.status_code, 201)  # 201 Created
        self.assertEqual(response.json()['name'], self.test_case_data['name'])

    def test_list_test_cases(self):
        TestCase.objects.create(**self.test_case_data)
        response = self.client.get(reverse('list_test_cases'))
        self.assertEqual(response.status_code, 200)  # 200 OK
        self.assertEqual(len(response.json()), 1)

    def test_get_test_case(self):
        test_case = TestCase.objects.create(**self.test_case_data)
        response = self.client.get(reverse('get_test_case', args=[test_case.id]))
        self.assertEqual(response.status_code, 200)  # 200 OK
        self.assertEqual(response.json()['id'], test_case.id)

    def test_update_test_case(self):
        test_case = TestCase.objects.create(**self.test_case_data)
        updated_data = {"name": "Updated Test Case"}
        response = self.client.put(reverse('update_test_case', args=[test_case.id]), json=updated_data)
        self.assertEqual(response.status_code, 200)  # 200 OK
        self.assertEqual(response.json()['name'], updated_data['name'])

    def test_delete_test_case(self):
        test_case = TestCase.objects.create(**self.test_case_data)
        response = self.client.delete(reverse('delete_test_case', args=[test_case.id]))
        self.assertEqual(response.status_code, 204)  # 204 No Content

    def test_create_test_job(self):
        response = self.client.post(reverse('create_test_job'), json=self.test_job_data)
        self.assertEqual(response.status_code, 201)  # 201 Created
        self.assertEqual(response.json()['name'], self.test_job_data['name'])

    def test_list_test_jobs(self):
        TestJob.objects.create(**self.test_job_data)
        response = self.client.get(reverse('list_test_jobs'))
        self.assertEqual(response.status_code, 200)  # 200 OK
        self.assertEqual(len(response.json()), 1)

    def test_get_test_job(self):
        job = TestJob.objects.create(**self.test_job_data)
        response = self.client.get(reverse('get_test_job', args=[job.id]))
        self.assertEqual(response.status_code, 200)  # 200 OK
        self.assertEqual(response.json()['id'], job.id)

    def test_update_test_job(self):
        job = TestJob.objects.create(**self.test_job_data)
        updated_data = {"name": "Updated Test Job"}
        response = self.client.put(reverse('update_test_job', args=[job.id]), json=updated_data)
        self.assertEqual(response.status_code, 200)  # 200 OK
        self.assertEqual(response.json()['name'], updated_data['name'])

    def test_delete_test_job(self):
        job = TestJob.objects.create(**self.test_job_data)
        response = self.client.delete(reverse('delete_test_job', args=[job.id]))
        self.assertEqual(response.status_code, 204)  # 204 No Content
