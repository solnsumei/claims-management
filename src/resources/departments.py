from .crudrouter import CrudRouter
from src.models import Department, DepartmentPydantic, DepartmentWithRelations
from src.models.schema.department import DepartmentSchema


router = CrudRouter(
    model=Department,
    response_schema=DepartmentPydantic,
    request_schema=DepartmentSchema,
    single_response_schema=DepartmentWithRelations,
)

router.load_routes()
