from .crudrouter import CrudRouter
from src.models import Project, ProjectPydantic, ProjectWithRelations, User
from src.models.schema.project import CreateSchema, UpdateSchema, AttachUsersSchema
from src.utils.enums import TeamAction
from src.utils.exceptions import UnProcessableException


router = CrudRouter(
    model=Project,
    request_schema=CreateSchema,
    response_schema=ProjectPydantic,
    single_response_schema=ProjectWithRelations,
    update_schema=UpdateSchema,
)

router.load_routes()


@router.put("/{item_id}/assign-team", response_model=ProjectWithRelations)
async def assign_team(item_id: str, schema: AttachUsersSchema):
    if len(schema.user_ids) > 0:
        project = await Project.get(id=item_id)

        members = await User.find_by(id__in=schema.user_ids)
        if schema.action == TeamAction.ADD:
            await project.team.add(*members)
        else:
            await project.team.remove(*members)

        return await ProjectWithRelations.from_tortoise_orm(project)

    raise UnProcessableException("No values provided to update")
