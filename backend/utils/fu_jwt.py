# backend/utils/fu_jwt.py
import jwt
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from django.conf import settings
from django.http import HttpRequest
from .fu_exception import AuthenticationError

# 从settings获取密钥和过期时间
JWT_SECRET = getattr(settings, "JWT_SECRET", "your-secret-key")
JWT_ALGORITHM = getattr(settings, "JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 60)
REFRESH_TOKEN_EXPIRE_DAYS = getattr(settings, "REFRESH_TOKEN_EXPIRE_DAYS", 7)


def create_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """创建JWT令牌"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def create_access_token(user_id: int, roles: list = None) -> str:
    """创建访问令牌"""
    return create_token(
        {"user_id": user_id, "roles": roles or [], "token_type": "access"},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(user_id: int) -> str:
    """创建刷新令牌"""
    return create_token(
        {"user_id": user_id, "token_type": "refresh"},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )


def decode_token(token: str) -> Dict[str, Any]:
    """解码并验证令牌"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError as e:
        raise AuthenticationError(f"无效的令牌: {str(e)}")


def get_token_from_request(request: HttpRequest) -> Optional[str]:
    """从请求中获取令牌"""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    return None
