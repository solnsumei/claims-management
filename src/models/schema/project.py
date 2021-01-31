from typing import Optional
from pydantic import Field, UUID4
from .baseschema import NameDescriptionSchema


class CreateSchema(NameDescriptionSchema):
    code: str = Field(..., min_length=2, max_length=15)
    manager_id: UUID4
    budget: int = Field(..., gt=0)
    duration: int = Field(..., gt=0)
    department_id: Optional[UUID4]


class UpdateSchema(NameDescriptionSchema):
    name: Optional[str] = Field(None, min_length=3, max_length=70, description="Name is required")
    description: Optional[str]
    manager_id: Optional[UUID4]
    budget: Optional[int] = Field(None, gt=0)
    duration: Optional[int] = Field(None, gt=0)
    department_id: Optional[UUID4]
