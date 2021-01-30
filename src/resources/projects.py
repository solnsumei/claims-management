from .crudrouter import CrudRouter
from src.models import Project, ProjectPydantic, ProjectWithRelations
from src.models.schema.project import ProjectSchema


router = CrudRouter(
    model=Project,
    request_schema=ProjectSchema,
    response_schema=ProjectPydantic,
    single_response_schema=ProjectWithRelations
)

router.load_routes()
