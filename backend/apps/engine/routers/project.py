from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from ..models import Project, Environment, VariableSet, Database
from .schemas import (
    ProjectSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
    EnvironmentSchema,
    EnvironmentCreateSchema,
    EnvironmentUpdateSchema,
    VariableSetSchema,
    VariableSetCreateSchema,
    VariableSetUpdateSchema,
    DatabaseSchema,
    DatabaseCreateSchema,
    DatabaseUpdateSchema
)

router = Router()

# ===== 项目管理 =====
@router.post("/projects/", response=ProjectSchema)
def create_project(request, data: ProjectCreateSchema):
    project = Project.objects.create(**data.dict())
    return project

@router.get("/projects/", response=List[ProjectSchema])
def list_projects(request):
    return Project.objects.all()

@router.get("/projects/{project_id}/", response=ProjectSchema)
def get_project(request, project_id: int):
    return get_object_or_404(Project, id=project_id)

@router.put("/projects/{project_id}/", response=ProjectSchema)
def update_project(request, project_id: int, data: ProjectUpdateSchema):
    project = get_object_or_404(Project, id=project_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(project, key, value)
    project.save()
    return project

@router.delete("/projects/{project_id}/")
def delete_project(request, project_id: int):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return {"success": True}

# ===== 环境管理 =====
@router.post("/environments/", response=EnvironmentSchema)
def create_environment(request, data: EnvironmentCreateSchema):
    environment = Environment.objects.create(**data.dict())
    return environment

@router.get("/environments/", response=List[EnvironmentSchema])
def list_environments(request):
    return Environment.objects.all()

@router.get("/environments/{environment_id}/", response=EnvironmentSchema)
def get_environment(request, environment_id: int):
    return get_object_or_404(Environment, id=environment_id)

@router.put("/environments/{environment_id}/", response=EnvironmentSchema)
def update_environment(request, environment_id: int, data: EnvironmentUpdateSchema):
    environment = get_object_or_404(Environment, id=environment_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(environment, key, value)
    environment.save()
    return environment

@router.delete("/environments/{environment_id}/")
def delete_environment(request, environment_id: int):
    environment = get_object_or_404(Environment, id=environment_id)
    environment.delete()
    return {"success": True}

# ===== 变量集管理 =====
@router.post("/variable-sets/", response=VariableSetSchema)
def create_variable_set(request, data: VariableSetCreateSchema):
    variable_set = VariableSet.objects.create(**data.dict())
    return variable_set

@router.get("/variable-sets/", response=List[VariableSetSchema])
def list_variable_sets(request):
    return VariableSet.objects.all()

@router.get("/variable-sets/{variable_set_id}/", response=VariableSetSchema)
def get_variable_set(request, variable_set_id: int):
    return get_object_or_404(VariableSet, id=variable_set_id)

@router.put("/variable-sets/{variable_set_id}/", response=VariableSetSchema)
def update_variable_set(request, variable_set_id: int, data: VariableSetUpdateSchema):
    variable_set = get_object_or_404(VariableSet, id=variable_set_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(variable_set, key, value)
    variable_set.save()
    return variable_set

@router.delete("/variable-sets/{variable_set_id}/")
def delete_variable_set(request, variable_set_id: int):
    variable_set = get_object_or_404(VariableSet, id=variable_set_id)
    variable_set.delete()
    return {"success": True}

# ===== 数据库管理 =====
@router.post("/databases/", response=DatabaseSchema)
def create_database(request, data: DatabaseCreateSchema):
    database = Database.objects.create(**data.dict())
    return database

@router.get("/databases/", response=List[DatabaseSchema])
def list_databases(request):
    return Database.objects.all()

@router.get("/databases/{database_id}/", response=DatabaseSchema)
def get_database(request, database_id: int):
    return get_object_or_404(Database, id=database_id)

@router.put("/databases/{database_id}/", response=DatabaseSchema)
def update_database(request, database_id: int, data: DatabaseUpdateSchema):
    database = get_object_or_404(Database, id=database_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(database, key, value)
    database.save()
    return database

@router.delete("/databases/{database_id}/")
def delete_database(request, database_id: int):
    database = get_object_or_404(Database, id=database_id)
    database.delete()
    return {"success": True}
