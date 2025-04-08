# engine/api/__init__.py
from ninja import Router
from . import testcase, project

router = Router()
router.add_router("/testcases", testcase.router)
router.add_router("/projects", project.router)
