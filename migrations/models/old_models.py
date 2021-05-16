from .base.basemodel import BaseModel, fields
from src.utils.enums import InvoiceStatus


class Claim(BaseModel):
    claim_id = fields.CharField(max_length=20, unique=True)
    invoice_no = fields.CharField(max_length=12)
    description = fields.TextField()
    amount = fields.DecimalField(decimal_places=2, max_digits=12)
    tax_percent = fields.DecimalField(decimal_places=2, max_digits=12, null=True)
    tax = fields.DecimalField(decimal_places=2, max_digits=12, null=True)
    approval_date = fields.DatetimeField(null=True)
    payment_date = fields.DateField(null=True)
    due_date = fields.DateField(null=True)
    file_url = fields.CharField(max_length=255, null=True)
    user = fields.ForeignKeyField('diff_models.User', related_name='claims', on_delete=fields.RESTRICT)
    project = fields.ForeignKeyField('diff_models.Project', related_name='claims', null=True, on_delete=fields.SET_NULL)
    department = fields.ForeignKeyField(
        'diff_models.Department', related_name='claims', null=True, on_delete=fields.SET_NULL)
    status = fields.CharEnumField(InvoiceStatus, default=InvoiceStatus.New)
    remark = fields.TextField(null=True)

    class Meta:
        table = 'claims'
        unique_together = (('user_id', 'invoice_no'), )

    class PydanticMeta:
        allow_cycles = False
        max_recursion = 0

from .base.basemodel import ModelWithStatus, fields


class Department(ModelWithStatus):
    name = fields.CharField(max_length=70, unique=True)
    # manager = fields.ForeignKeyField('diff_models.User', related_name='departments', null=True)

    class Meta:
        table = 'departments'
        ordering = ['created_at', 'name']

    class PydanticMeta:
        allow_cycles = False
        max_recursion = 0

from .base.basemodel import ModelWithStatus, fields


class Project(ModelWithStatus):
    name = fields.CharField(max_length=70)
    code = fields.CharField(max_length=15, unique=True)
    description = fields.TextField()
    manager = fields.ForeignKeyField('diff_models.User', related_name='managed_projects', on_delete=fields.RESTRICT)
    department = fields.ForeignKeyField(
        'diff_models.Department', related_name='projects', null=True, on_delete=fields.SET_NULL)
    budget = fields.DecimalField(decimal_places=2, max_digits=12)
    duration = fields.IntField()
    team = fields.ManyToManyField('diff_models.User', related_name='projects', null=True)

    class Meta:
        table = 'projects'
        ordering = ['created_at', 'code']

    class PydanticMeta:
        allow_cycles = False
        max_recursion = 0

from passlib.context import CryptContext
from .base.basemodel import ModelWithStatus, fields
from src.utils.enums import Role

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(ModelWithStatus):
    name = fields.CharField(max_length=50)
    username = fields.CharField(max_length=30, unique=True)
    email = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=250)
    is_admin = fields.BooleanField(default=False)
    role = fields.CharEnumField(Role, default=Role.Staff)
    department = fields.ForeignKeyField(
        'diff_models.Department', related_name='employees', null=True, on_delete=fields.SET_NULL)
    uses_default_password = fields.BooleanField(default=True)

    @classmethod
    async def find_by_email(cls, email):
        return await cls.filter(email=email).first()

    @classmethod
    async def find_by_username(cls, username):
        return await cls.filter(username=username).first()

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






from tortoise import Model, fields

MAX_VERSION_LENGTH = 255


class Aerich(Model):
    version = fields.CharField(max_length=MAX_VERSION_LENGTH)
    app = fields.CharField(max_length=20)
    content = fields.TextField()

    class Meta:
        ordering = ["-id"]

