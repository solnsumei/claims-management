from fastapi import Depends
from src.models import UserPydantic
from src.models.schema.user import AuthSchema
from src.utils.security import create_token, authenticate, get_current_user
from .baserouter import BaseRouter


router = BaseRouter()


@router.post('/login')
async def login_user(auth: AuthSchema):
    user = await authenticate(auth.username, auth.password)
    token = create_token({
        "username": user.username,
        "isAdmin": user.is_admin,
        'role': user.role
    })

    user_pydantic = await UserPydantic.from_tortoise_orm(user)

    return {
        "user": user_pydantic,
        "token": token
    }


@router.get('/user')
async def profile(user: dict = Depends(get_current_user)):
    logged_in_user = await UserPydantic.from_tortoise_orm(user)
    return {
        "user": logged_in_user,
    }
