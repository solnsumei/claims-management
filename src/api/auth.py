from src.models import UserPydantic
from src.models.schema.user import AuthSchema
from src.utils.security import create_token, authenticate
from .baserouter import APIRouter


router = APIRouter()


@router.post('/login')
async def login_user(auth: AuthSchema):
    user = await authenticate(auth.username, auth.password)
    token = create_token({"sub": user.username})

    user_pydantic = await UserPydantic.from_tortoise_orm(user)

    return {
        "user": user_pydantic,
        "token": token
    }

