from fastapi import Depends
from src.models import User, UserWithDepartment
from src.models.schema.user import AuthSchema, ChangePasswordSchema
from src.utils.security import create_token, authenticate, get_current_user
from .baserouter import BaseRouter
from src.utils.enums import EmployeeRole
from src.utils.exceptions import UnProcessableException


router = BaseRouter()


@router.post('/login')
async def login_user(auth: AuthSchema):
    user = await authenticate(auth.email, auth.password)
    token = create_token({
        "name": user.name,
        "email": user.email,
        "isAdmin": user.is_admin,
        'role': user.role
    })

    user_pydantic = await UserWithDepartment.from_tortoise_orm(user)

    return {
        "user": user_pydantic,
        "token": token
    }


@router.post('/change-password')
async def change_password(
        passwords: ChangePasswordSchema,
        update: bool = False,
        auth: User = Depends(get_current_user)
):

    if update is True:
        if passwords.old_password is None or not User.verify_hash(passwords.old_password, auth.password):
            raise UnProcessableException(['old_password', 'Old password is incorrect'])

    if passwords.password != passwords.password_confirmation:
        raise UnProcessableException(['password', 'Passwords does not match'])

    auth.password = User.generate_hash(passwords.password)

    if update is False:
        auth.uses_default_password = False
    await auth.save()

    await auth.refresh_from_db(fields=['uses_default_password', 'password'])
    return await UserWithDepartment.from_tortoise_orm(auth)


@router.get('/roles', dependencies=[Depends(get_current_user)])
async def employee_roles():
    return list(EmployeeRole)
