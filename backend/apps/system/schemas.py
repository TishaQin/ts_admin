from typing import List, Optional
from ninja import Schema
from datetime import datetime


class UserSchema(Schema):
    id: int
    username: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    date_joined: datetime


class RoleSchema(Schema):
    id: int
    name: str
    description: Optional[str] = None


class MenuSchema(Schema):
    id: int
    name: str
    parent_id: Optional[int] = None
    path: Optional[str] = None
    component: Optional[str] = None
    icon: Optional[str] = None
    sort: int = 0
    is_visible: bool = True
