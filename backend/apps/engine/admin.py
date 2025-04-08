from django.contrib import admin
from .models import *

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at", "created_by", "updated_by")
    search_fields = ("name",)

@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "base_url", "project", "created_at")
    list_filter = ("project",)
    search_fields = ("name", "base_url")

@admin.register(VariableSet)
class VariableSetAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "project")
    search_fields = ("name",)

@admin.register(Database)
class DatabaseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "db_type", "host", "port", "username", "project")
    search_fields = ("name", "host")

@admin.register(ApiInterface)
class ApiInterfaceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "method", "url", "protocol", "project")
    search_fields = ("name", "url")

@admin.register(TestSuite)
class TestSuiteAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "project", "is_public", "parent")

@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "protocol", "project", "environment", "suite")
    list_filter = ("protocol", "project")

@admin.register(TestStep)
class TestStepAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "testcase", "action_type", "order", "api_interface")

@admin.register(TestJob)
class TestJobAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "run_mode", "suite", "environment")

@admin.register(SchedulePlan)
class SchedulePlanAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "cron", "job", "enabled")

@admin.register(CeleryTaskRecord)
class CeleryTaskRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "job", "task_id", "status", "started_at", "finished_at")

@admin.register(TestReport)
class TestReportAdmin(admin.ModelAdmin):
    list_display = ("id", "job", "report_type", "created_at")

@admin.register(CaseReport)
class CaseReportAdmin(admin.ModelAdmin):
    list_display = ("id", "report", "testcase", "status", "duration")

@admin.register(StepReport)
class StepReportAdmin(admin.ModelAdmin):
    list_display = ("id", "case_report", "step", "status", "duration")

@admin.register(HookTemplate)
class HookTemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "hook_type", "language")

@admin.register(CustomAssertion)
class CustomAssertionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(ExceptionCategory)
class ExceptionCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(ExceptionRecord)
class ExceptionRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "job", "source")

@admin.register(ToolFunction)
class ToolFunctionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "language")

@admin.register(DataGenerator)
class DataGeneratorAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
