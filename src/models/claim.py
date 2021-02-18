from .base.basemodel import BaseModel, fields
from src.utils.enums import InvoiceStatus


class Claim(BaseModel):
    title = fields.CharField(max_length=100)
    claim_id = fields.CharField(max_length=20, unique=True)
    invoice_no = fields.CharField(max_length=12, unique=True)
    description = fields.TextField()
    amount = fields.DecimalField(decimal_places=2, max_digits=12)
    approval_date = fields.DatetimeField(null=True)
    payment_date = fields.DateField(null=True)
    due_date = fields.DateField(null=True)
    file_url = fields.CharField(max_length=255, null=True)
    user = fields.ForeignKeyField('models.User', related_name='claims')
    project = fields.ForeignKeyField('models.Project', related_name='claims', null=True)
    department = fields.ForeignKeyField('models.Department', related_name='claims', null=True)
    status = fields.CharEnumField(InvoiceStatus, default=InvoiceStatus.New)
    remark = fields.TextField(null=True)

    class Meta:
        table = 'claims'

    class PydanticMeta:
        allow_cycles = False
        max_recursion = 0
