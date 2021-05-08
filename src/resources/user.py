from fastapi import Depends
from tortoise.query_utils import Q
from src.models import User, UserWithDepartment,  Project, ProjectWithTeam, ProjectDefault
from src.utils.security import get_current_user
from src.utils.enums import Role
from .baserouter import BaseRouter


router = BaseRouter()


@router.get('/')
async def profile(logged_in_user: dict = Depends(get_current_user)):
    user = await UserWithDepartment.from_tortoise_orm(logged_in_user)
    return {
        "user": user,
    }


@router.get('/projects')
async def fetch_projects(user: User = Depends(get_current_user)):
    if user.is_admin or user.role == Role.Admin:
        projects = await ProjectWithTeam.from_queryset(Project.all())
    elif user.role == Role.Manager:
        projects = await ProjectWithTeam.from_queryset(
            Project.filter(Q(team__id=user.id) | Q(manager__id=user.id))
        )
    else:
        projects = await ProjectDefault.from_queryset(Project.filter(team__id=user.id))

    return projects
