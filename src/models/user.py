from passlib.context import CryptContext
from .base.basemodel import ModelWithStatus, fields
from src.utils.enums import Role

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(ModelWithStatus):
    name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=250)
    is_admin = fields.BooleanField(default=False)
    role = fields.CharEnumField(Role, default=Role.Staff)
    department = fields.ForeignKeyField(
        'models.Department', related_name='employees', null=True, on_delete=fields.SET_NULL)
    uses_default_password = fields.BooleanField(default=True)

    @classmethod
    async def find_by_email(cls, email):
        return await cls.filter(email=email).first()

    @staticmethod
    def generate_hash(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def verify_hash(password: str, hashed_password: str):
        return pwd_context.verify(password, hashed_password)

    class Meta:
        table = "users"
        ordering = ['created_at', 'name']

    class PydanticMeta:
        exclude = ['password']
        max_recursion = 0
        allow_cycles = False





