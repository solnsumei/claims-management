from typing import Optional
from pydantic import Field, UUID4
from .baseschema import NameDescriptionSchema


class ProjectSchema(NameDescriptionSchema):
    code: str = Field(..., min_length=2, max_length=15)
    manager_id: UUID4
    budget: int = Field(..., gt=0)
    duration: int = Field(..., gt=0)
    department_id: Optional[UUID4]
