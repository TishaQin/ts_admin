from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    """扩展用户模型"""

    avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True, verbose_name="头像"
    )
    phone = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="手机号"
    )

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"


class Role(models.Model):
    """角色模型"""

    name = models.CharField(max_length=100, unique=True, verbose_name="角色名称")
    description = models.TextField(null=True, blank=True, verbose_name="描述")
    permissions = models.ManyToManyField(Permission, blank=True, verbose_name="权限")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = "角色"

    def __str__(self):
        return self.name


class Menu(models.Model):
    """菜单模型"""

    name = models.CharField(max_length=100, verbose_name="菜单名称")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="父菜单",
    )
    path = models.CharField(max_length=200, null=True, blank=True, verbose_name="路径")
    component = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="组件"
    )
    icon = models.CharField(max_length=100, null=True, blank=True, verbose_name="图标")
    sort = models.IntegerField(default=0, verbose_name="排序")
    is_visible = models.BooleanField(default=True, verbose_name="是否可见")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "菜单"
        verbose_name_plural = "菜单"
        ordering = ["sort"]

    def __str__(self):
        return self.name


class ApiLog(models.Model):
    """API日志模型"""

    """API日志模型类 - 如果选择存储到数据库"""

    request_username = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="请求用户"
    )
    request_ip = models.CharField(max_length=50, verbose_name="请求IP")
    request_method = models.CharField(max_length=20, verbose_name="请求方法")
    request_path = models.CharField(max_length=255, verbose_name="请求路径")
    request_body = models.JSONField(null=True, verbose_name="请求参数")
    request_time = models.DateTimeField(auto_now_add=True, verbose_name="请求时间")
    response_code = models.IntegerField(null=True, verbose_name="响应状态码")
    response_body = models.JSONField(null=True, verbose_name="响应内容")
    execution_time = models.FloatField(default=0, verbose_name="执行时间(ms)")
    request_os = models.CharField(max_length=100, null=True, verbose_name="操作系统")
    request_browser = models.CharField(max_length=100, null=True, verbose_name="浏览器")
    request_module = models.CharField(
        max_length=100, null=True, verbose_name="请求模块"
    )
    success = models.BooleanField(default=True, verbose_name="是否成功")

    class Meta:
        db_table = "fu_api_log"
        verbose_name = "API访问日志"
        verbose_name_plural = verbose_name
        ordering = ["-request_time"]
