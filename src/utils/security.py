from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends
from fastapi.security import HTTPBearer
from src.config.settings import Settings as Config
from src.models import User
from src.utils.enums import Role, Status
from .exceptions import UnauthorisedException, ForbiddenException


async def authenticate(username: str, password: str):
    user = await User.find_by_email(username)

    if user and User.verify_hash(password, user.password):
        if user.status != Status.ACTIVE:
            raise UnauthorisedException("Your account is inactive, please contact your manager")
        return user

    raise UnauthorisedException("Username and/or password is incorrect")


def check_token(auth_token=Depends(HTTPBearer(
    scheme_name="bearerAuth",
    bearerFormat="JWT",
    auto_error=False,
))):
    """
    Check valid token
    :param auth_token:
    :return: str
    """
    if auth_token is None:
        raise UnauthorisedException()

    try:
        payload = jwt.decode(
            auth_token.credentials,
            Config.SECRET_KEY,
            algorithms=[Config.ALGORITHM]
        )

        username: str = payload.get("email")
        if username is None:
            raise JWTError
    except JWTError:
        raise UnauthorisedException("Access token is invalid")
    return username


async def get_current_user(username: str = Depends(check_token)):
    """
    Fetch logged in user from database
    :param username:
    :return: User
    """
    user = await User.find_by_email(username)
    if user is None:
        raise UnauthorisedException("Access token is invalid")
    return user


async def check_admin_or_manager(user: User = Depends(get_current_user)):
    """
    Check if user is an admin
    :param user:
    :return: User
    """
    if user.role != Role.Manager and user.role != Role.Admin and not user.is_admin:
        raise ForbiddenException()
    return user


async def check_admin(user: User = Depends(get_current_user)):
    """
    Check if user is an admin
    :param user:
    :return: User
    """
    if user.role != Role.Admin.value and not user.is_admin:
        raise ForbiddenException()
    return user


def create_token(data: dict, expiry: Optional[timedelta] = None):
    to_encode = data.copy()

    if expiry:
        expire = datetime.utcnow() + expiry
    else:
        expire = datetime.utcnow()\
                 + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)

    return token
