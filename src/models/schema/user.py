from typing import Optional
from pydantic import EmailStr, Field, UUID4
from .baseschema import BaseSchema, StatusSchema, NameSchema
from src.utils.enums import Role, Status


class AuthSchema(BaseSchema):
    email: EmailStr
    password: str


class ChangePasswordSchema(BaseSchema):
    old_password: Optional[str]
    password: str = Field(..., min_length=8, max_length=70)
    password_confirmation: str = Field(..., min_length=8, max_length=70)


class CreateSchema(NameSchema):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=70)
    role: Optional[Role] = Field(Role.Staff)
    department_id: Optional[UUID4]
    status:  Optional[Status] = Field(Status.INACTIVE)


class UpdateSchema(StatusSchema):
    name: Optional[str] = Field(None, min_length=3, max_length=70)
    email: Optional[EmailStr]
    password: str = Field(None, min_length=8, max_length=70)
    role: Optional[Role]
    department_id: Optional[UUID4]
    status: Optional[Status]
