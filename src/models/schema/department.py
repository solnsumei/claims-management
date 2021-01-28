from typing import Optional
from pydantic import Field
from .baseschema import StatusSchema


class DepartmentSchema(StatusSchema):
    name: str = Field(..., min_length=2, max_length=30)
