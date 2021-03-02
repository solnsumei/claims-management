from fastapi import Depends, BackgroundTasks
from .baserouter import BaseRouter
from src.models import User, UserWithDepartment, UserWithRelations
from src.models.schema.user import CreateSchema, UpdateSchema
from src.utils.security import check_admin
from src.utils.exceptions import ForbiddenException
from src.services.mail_service import mail_service, create_welcome_message
from src.utils.enums import EmployeeRole


router = BaseRouter()


@router.get("/", response_model=list[UserWithDepartment])
async def fetch_all_staff(contractors: bool = False, auth: User = Depends(check_admin)):
    employees_list = list(EmployeeRole)
    if auth.is_admin:
        if contractors:
            return await User.find_by("department", role__not_in=employees_list)
        return await User.find_by("department", role__in=employees_list)
    return await User.find_by("department", is_admin=False)


@router.get("/{user_id}", response_model=UserWithRelations)
async def get_user(user_id: str, auth: User = Depends(check_admin)):
    if auth.is_admin:
        return await UserWithRelations.from_queryset_single(User.get(id=user_id))
    return await UserWithRelations.from_queryset_single(User.get(is_admin=False, id=user_id))


@router.post("/", status_code=201, response_model=UserWithDepartment,
             dependencies=[Depends(check_admin)])
async def add_user(user: CreateSchema, background_tasks: BackgroundTasks):
    password = user.password
    user.password = User.generate_hash(password)
    new_user = await User.create_one(user)

    if user.project_id is not None:
        new_user.projects.add(project_id=user.project_id)

    message = create_welcome_message(
        name=user.name,
        email=[user.email],
        password=password,
    )

    background_tasks.add_task(mail_service.send_message, message)
    return await UserWithDepartment.from_tortoise_orm(new_user)


@router.put("/{user_id}", response_model=UserWithDepartment)
async def update_user(user_id: str, user_schema: UpdateSchema, auth: User = Depends(check_admin)):
    found_user = await User.find_one(id=user_id)

    if found_user.is_admin and found_user.id != auth.id:
        raise ForbiddenException(message="You cannot update an admin")

    if auth.is_admin:
        updated_item = await User.update_one(user_id, user_schema)
        return await UserWithDepartment.from_queryset_single(updated_item)

    if found_user.role == "Admin":
        raise ForbiddenException(message="You cannot update an admin")

    updated_item = await User.update_one(user_id, user_schema)
    return await UserWithDepartment.from_queryset_single(updated_item)


@router.delete("/{user_id}")
async def delete_user(user_id: str, auth: User = Depends(check_admin)):
    if auth.id == user_id:
        raise ForbiddenException(message="You cannot delete yourself")

    user = await User.find_one(id=user_id)

    if user.is_admin:
        raise ForbiddenException("You cannot delete an admin")

    success_message = {"message": "Item deleted successfully"}

    if auth.is_admin:
        await User.delete_one(user_id)
        return success_message

    if user.role == "Admin":
        raise ForbiddenException("You cannot delete an admin")

    await User.delete_one(user_id)
    return success_message
