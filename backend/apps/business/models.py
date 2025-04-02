from django.db import models
from apps.system.models import User
from .schemas import ACTIVITY_STATUS_CHOICES, PARTICIPANT_STATUS_CHOICES


class ActivityType(models.Model):
    """活动类型模型"""

    name = models.CharField(max_length=100, verbose_name="类型名称")
    description = models.TextField(null=True, blank=True, verbose_name="描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "活动类型"
        verbose_name_plural = "活动类型"

    def __str__(self):
        return self.name


class Activity(models.Model):
    """活动模型"""

    title = models.CharField(max_length=200, verbose_name="活动标题")
    description = models.TextField(verbose_name="活动描述")
    start_time = models.DateTimeField(verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="结束时间")
    location = models.CharField(max_length=200, verbose_name="活动地点")
    max_participants = models.PositiveIntegerField(
        default=0, verbose_name="最大参与人数", help_text="0表示不限制"
    )
    current_participants = models.PositiveIntegerField(
        default=0, verbose_name="当前参与人数"
    )
    activity_type = models.ForeignKey(
        ActivityType,
        on_delete=models.CASCADE,
        related_name="activities",
        verbose_name="活动类型",
    )
    cover_image = models.ImageField(
        upload_to="activity_covers/", null=True, blank=True, verbose_name="封面图片"
    )
    status = models.CharField(
        max_length=20,
        choices=ACTIVITY_STATUS_CHOICES,
        default="draft",
        verbose_name="状态",
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_activities",
        verbose_name="创建者",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "活动"
        verbose_name_plural = "活动"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ActivityParticipant(models.Model):
    """活动参与者模型"""

    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name="participants",
        verbose_name="活动",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="participating_activities",
        verbose_name="用户",
    )
    status = models.CharField(
        max_length=20,
        choices=PARTICIPANT_STATUS_CHOICES,
        default="registered",
        verbose_name="状态",
    )
    register_time = models.DateTimeField(auto_now_add=True, verbose_name="报名时间")
    remark = models.TextField(null=True, blank=True, verbose_name="备注")

    class Meta:
        verbose_name = "活动参与者"
        verbose_name_plural = "活动参与者"
        unique_together = ("activity", "user")

    def __str__(self):
        return f"{self.user.username} - {self.activity.title}"
