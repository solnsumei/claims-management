from typing import Optional
from pydantic import EmailStr, Field, UUID4
from .baseschema import BaseSchema, NameSchema
from src.utils.enums import Role


class AuthSchema(BaseSchema):
    username: str
    password: str


class UserSchema(NameSchema):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=8, max_length=70)
    role: Optional[Role] = Field(Role.Staff)
    department_id: Optional[UUID4]
