# 如果完全不需要在管理后台显示这些模型，可以留空文件或只保留导入语句：
from django.contrib import admin
from .models import ActivityType, Activity, ActivityParticipant

# 只注册模型，不添加自定义配置
admin.site.register(ActivityType)
admin.site.register(Activity)
admin.site.register(ActivityParticipant)
