from fastapi import Depends
from src.models import UserPydantic, User, UserWithDepartment
from src.utils.security import get_current_user
from .baserouter import BaseRouter


router = BaseRouter()


@router.get('/profile')
async def profile(logged_in_user: dict = Depends(get_current_user)):
    user = await UserWithDepartment.from_tortoise_orm(logged_in_user)
    return {
        "user": user,
    }

