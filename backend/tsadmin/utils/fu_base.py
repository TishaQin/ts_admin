# backend/utils/fu_base.py
from typing import Dict, Any, Optional
from datetime import datetime
import os
import json
import logging
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils import timezone
from django.db import models
import redis


class FuBase:
    """基础工具类"""

    def __init__(self):
        self.redis_client = self._get_redis_client()
        self.logger = self._get_logger()

    def _get_redis_client(self) -> redis.Redis:
        """获取 Redis 客户端"""
        return redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
        )

    def _get_logger(self) -> logging.Logger:
        """获取日志记录器"""
        logger = logging.getLogger("api")
        return logger

    def get_cache(self, key: str, default: Any = None) -> Any:
        """获取缓存值"""
        value = self.redis_client.get(key)
        return json.loads(value) if value else default

    def set_cache(self, key: str, value: Any, expire: int = None) -> bool:
        """设置缓存值"""
        value_str = json.dumps(value)
        return self.redis_client.set(key, value_str, ex=expire)
