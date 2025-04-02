使用 Django Ninja 构建 API
使用 JWT 进行身份认证
使用 Redis 做缓存
使用 Celery 处理异步任务
使用 Django CORS headers 处理跨域
使用 Django Filter 处理数据过滤
使用 Django Swagger 生成 API 文档
使用环境变量管理敏感信息
实现请求频率限制
实现 IP 白名单
实现操作日志记录
实现数据备份机制
实现完整的日志系统
处理文件上传和管理

使用开源系统三选一，给出选择理由：
Django Simple UI
Django Xadmin
Django Jet

并提供一个代码生成器的模块
提高开发效率：自动生成 CRUD 相关代码
保持代码规范：统一的代码风格和结构
减少重复工作：避免手动编写相似的代码
易于维护：生成的代码结构清晰，易于修改
Generator 代码生成器功能：
代码生成器模板（GeneratorTemplate）：
支持自定义表单信息
支持自定义表格信息
支持自动生成菜单
使用方法：
在后台创建代码生成器模板
配置表单字段和表格列
选择是否生成菜单
系统会自动生成：
模型文件（models.py）
序列化器（serializers.py）
视图（views.py）
API 接口（apis.py）
路由配置（urls.py）
前端页面（Vue 组件）

backend/
├── apps/ # 应用目录
│ ├── system/ # 系统管理
│ ├── business/ # 业务模块
│ └── common/ # 公共模块
├── utils/ # 工具类
├── config/ # 配置文件
├── static/ # 静态文件
├── media/ # 媒体文件
└── templates/ # 模板文件
