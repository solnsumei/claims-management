from typing import Optional, List
from pydantic import BaseModel, UUID4


class BaseProjectSchema(BaseModel):
    id: UUID4
    name: str
    description: str
    manager: dict
    budget: int
    duration: int
    department: dict
