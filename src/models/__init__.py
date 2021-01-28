from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from .user import User
from .project import Project
from .department import Department
from .claim import Claim


# Initialize model relationships
Tortoise.init_models(["src.models"], "models")

# User serialization
UserPydantic = pydantic_model_creator(User)
UserWithRelations = pydantic_model_creator(User, name="UserWithRelations")
