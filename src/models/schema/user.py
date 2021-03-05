from typing import Optional
from pydantic import EmailStr, Field, UUID4
from .baseschema import BaseSchema, StatusSchema, NameSchema
from src.utils.enums import Role


class AuthSchema(BaseSchema):
    username: str
    password: str


class CreateSchema(NameSchema):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=8, max_length=70)
    role: Optional[Role] = Field(Role.Staff)
    department_id: Optional[UUID4]


class UpdateSchema(StatusSchema):
    name: Optional[str] = Field(None, min_length=3, max_length=70)
    email: Optional[EmailStr]
    password: str = Field(None, min_length=8, max_length=70)
    role: Optional[Role]
    department_id: Optional[UUID4]
