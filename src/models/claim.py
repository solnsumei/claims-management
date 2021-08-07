from .base.basemodel import BaseModel, fields
from src.utils.enums import InvoiceStatus


class Claim(BaseModel):
    claim_id = fields.CharField(max_length=20, unique=True)
    invoice_no = fields.CharField(max_length=12)
    description = fields.TextField()
    amount = fields.DecimalField(decimal_places=2, max_digits=12)
    tax_percent = fields.DecimalField(decimal_places=2, max_digits=12, null=True)
    tax = fields.DecimalField(decimal_places=2, max_digits=12, null=True)
    approval_date = fields.DatetimeField(null=True)
    payment_date = fields.DateField(null=True)
    due_date = fields.DateField(null=True)
    file_url = fields.CharField(max_length=255, null=True)
    user = fields.ForeignKeyField('models.User', related_name='claims', on_delete=fields.RESTRICT)
    project = fields.ForeignKeyField('models.Project', related_name='claims', null=True, on_delete=fields.SET_NULL)
    department = fields.ForeignKeyField(
        'models.Department', related_name='claims', null=True, on_delete=fields.SET_NULL)
    status = fields.CharEnumField(InvoiceStatus, default=InvoiceStatus.New)
    remark = fields.TextField(null=True)

    class Meta:
        table = 'claims'
        unique_together = (('user_id', 'invoice_no'),)
        ordering = ['claim_id']

    class PydanticMeta:
        allow_cycles = False
        max_recursion = 0
