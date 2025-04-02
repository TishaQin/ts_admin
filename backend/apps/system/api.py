from ninja import Router
from typing import List
from django.http import HttpRequest

router = Router(tags=["system"])


@router.get("/")
def list_system_endpoints(request: HttpRequest):
    return {"message": "System API endpoints"}
