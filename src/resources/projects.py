from typing import List
from fastapi import Depends
from tortoise.functions import Sum

from .baserouter import BaseRouter
from src.models import Project, ProjectPydantic, ProjectWithRelations, User, Claim, ClaimWithRelations
from src.models.schema.project import CreateSchema, UpdateSchema, AttachUsersSchema
from src.utils.enums import TeamAction, Role
from src.utils.security import check_admin_or_manager, check_admin
from src.utils.exceptions import UnProcessableException


router = BaseRouter()


@router.get("/", response_model=List[ProjectPydantic])
async def fetch_all(auth: User = Depends(check_admin_or_manager)):
    if auth.role == Role.Manager:
        return await ProjectPydantic.from_queryset(
            Project.filter(manager__id=auth.id)
        )
    return await ProjectPydantic.from_queryset(Project.all())


@router.get("/{item_id}/claims", response_model=List[ClaimWithRelations],
            dependencies=[Depends(check_admin_or_manager)])
async def fetch_project_claims(item_id: str):
    return await ClaimWithRelations.from_queryset(
        Claim.filter(project__id=item_id)
    )


@router.get("/{item_id}/stats", dependencies=[Depends(check_admin_or_manager)])
async def fetch_claims_summary(item_id: str):
    return await Claim.filter(project__id=item_id).annotate(total=Sum('amount'))\
        .group_by('status').values("status", "total")


@router.get("/{item_id}", response_model=ProjectWithRelations)
async def fetch_one(item_id: str, auth: User = Depends(check_admin_or_manager)):
    if auth.role == Role.Manager:
        return await ProjectWithRelations.from_queryset_single(
            Project.get(manager__id=auth.id, id=item_id)
        )
    return await ProjectWithRelations.from_queryset_single(Project.get(id=item_id))


@router.post("/", status_code=201, response_model=ProjectPydantic,
             dependencies=[Depends(check_admin)])
async def create(item: CreateSchema):
    new_item = await Project.create_one(item)
    return await ProjectPydantic.from_tortoise_orm(new_item)


@router.put("/{item_id}", response_model=ProjectPydantic,
            dependencies=[Depends(check_admin)])
async def update(item_id: str, item: UpdateSchema):
    updated_item = await Project.update_one(item_id, item)
    return await ProjectPydantic.from_queryset_single(updated_item)


@router.delete("/{item_id}", dependencies=[Depends(check_admin)])
async def delete(item_id: str):
    await ProjectPydantic.delete_one(item_id)
    return {"message": "Item deleted successfully"}


@router.put("/{item_id}/assign-team", response_model=ProjectWithRelations)
async def assign_team(item_id: str, schema: AttachUsersSchema, auth: User = Depends(check_admin_or_manager)):
    if len(schema.user_ids) > 0:
        project = await Project.get(id=item_id)

        members = await User.find_by(id__in=schema.user_ids)
        if schema.action == TeamAction.ADD:
            await project.team.add(*members)
        else:
            if auth.role == Role.Manager:
                for member in members:
                    if member.role == Role.Admin:
                        raise UnProcessableException("You cannot delete an admin")
            await project.team.remove(*members)

        return await ProjectWithRelations.from_tortoise_orm(project)

    raise UnProcessableException("No values provided to update")
