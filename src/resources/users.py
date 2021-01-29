from fastapi import Depends
from .baserouter import BaseRouter
from src.models import User, UserPydantic
from src.models.schema.user import UserSchema
from src.utils.security import check_admin
from src.utils.exceptions import ForbiddenException


router = BaseRouter()


@router.get("/", response_model=list[UserPydantic])
async def fetch_all_staff(auth: User = Depends(check_admin)):
    if auth.is_admin:
        return await UserPydantic.from_queryset(User.all())
    return await UserPydantic.from_queryset(User.find_by(is_admin=False))


@router.get("/{user_id}", response_model=UserPydantic)
async def get_user(user_id: str, auth: User = Depends(check_admin)):
    if auth.is_admin:
        return await UserPydantic.from_queryset_single(User.get(id=user_id))
    return await UserPydantic.from_queryset_single(User.get(is_admin=False, id=user_id))


@router.post("/", status_code=201, response_model=UserPydantic,
             dependencies=[Depends(check_admin)])
async def add_user(user: UserSchema):
    new_user = await User.create_one(user)
    return await UserPydantic.from_tortoise_orm(new_user)


@router.put("/{user_id}", response_model=UserPydantic)
async def update_user(user_id: str, user_schema: UserSchema, auth: User = Depends(check_admin)):
    found_user = await User.find_one(id=user_id)

    if found_user.is_admin and found_user.id != auth.id:
        raise ForbiddenException(message="You cannot update an admin")

    if auth.is_admin:
        updated_item = await User.update_one(user_id, user_schema)
        return await UserPydantic.from_queryset_single(updated_item)

    if found_user.role == "Admin":
        raise ForbiddenException(message="You cannot update an admin")

    updated_item = await User.update_one(user_id, user_schema)
    return await UserPydantic.from_queryset_single(updated_item)


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
