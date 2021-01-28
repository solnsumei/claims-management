from .base.basemodel import ModelWithStatus, fields


class Project(ModelWithStatus):
    name = fields.CharField(max_length=70)
    code = fields.CharField(max_length=15, unique=True)
    description = fields.TextField()
    manager = fields.ForeignKeyField('models.User', related_name='managed_projects')
    department = fields.ForeignKeyField('models.Department', related_name='projects', null=True)
    budget = fields.DecimalField(decimal_places=2, max_digits=12)
    duration = fields.IntField()
    contractors = fields.ManyToManyField('models.User', related_name='projects', null=True)

    class Meta:
        table = 'projects'
