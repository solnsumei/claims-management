from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator


from .user import User
from .project import Project
from .department import Department
from .claim import Claim


# Initialize model relationships
Tortoise.init_models(["src.models"], "models")

# User serialization
UserPydantic = pydantic_model_creator(User, exclude=('managed_projects', 'claims', 'projects', 'department'))
UserWithDepartment = pydantic_model_creator(User, name="UserWithDepartment", exclude=(
    'claims', 'managed_projects', 'projects'))
UserWithDeptProjects = pydantic_model_creator(User, name="UserWithDeptProjects", exclude=('claims',))
UserWithRelations = pydantic_model_creator(User, name="UserWithRelations")


# Department serialization
DepartmentPydantic = pydantic_model_creator(Department, name="Department", exclude=('employees', 'claims', 'projects'))
DepartmentWithRelations = pydantic_model_creator(
    Department, name="DepartmentWithRelations"
)

# Project serialization
ProjectPydantic = pydantic_model_creator(Project, name="Project", exclude=(
    'claims', 'manager', 'department', 'team'))

ProjectWithTeam = pydantic_model_creator(
    Project, name="ProjectWithTeam", exclude=('claims',)
)

ProjectWithRelations = pydantic_model_creator(
    Project, name="ProjectWithRelations"
)

ProjectDefault = pydantic_model_creator(
    Project, name="ProjectDefault", exclude=('budget', 'claims', 'team'))

# Claim serialization
ClaimPydantic = pydantic_model_creator(Claim, name="Claim", exclude=(
    'project', 'department', 'user'))
ClaimWithRelations = pydantic_model_creator(
    Claim, name="ClaimWithRelations"
)
