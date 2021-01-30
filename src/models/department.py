from .base.basemodel import ModelWithStatus, fields


class Department(ModelWithStatus):
    name = fields.CharField(max_length=70, unique=True)
    # manager = fields.ForeignKeyField('models.User', related_name='departments', null=True)

    class Meta:
        table = 'departments'

    class PydanticMeta:
        allow_cycles = False
        max_recursion = 0
