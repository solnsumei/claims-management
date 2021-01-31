from .crudrouter import CrudRouter
from src.models import Project, ProjectPydantic, ProjectWithRelations
from src.models.schema.project import CreateSchema, UpdateSchema


router = CrudRouter(
    model=Project,
    request_schema=CreateSchema,
    response_schema=ProjectPydantic,
    single_response_schema=ProjectWithRelations,
    update_schema=UpdateSchema,
)

router.load_routes()
