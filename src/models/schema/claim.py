from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import Field, UUID4
from .baseschema import BaseSchema, DescriptionSchema
from src.utils.enums import InvoiceUpdateAction, InvoiceVerifyAction


class CreateSchema(DescriptionSchema):
    claim_id: Optional[str]
    user_id: Optional[UUID4]
    invoice_no: str = Field(..., min_length=2, max_length=15)
    amount: Decimal = Field(..., gt=0)
    department_id: Optional[UUID4]
    project_id: Optional[UUID4]
    due_date: Optional[date]

    # @validator("due_date", pre=True)
    # def parse_date(cls, value):
    #     if value is not None:
    #         return datetime.strptime(
    #             value,
    #             "%d/%m/%Y"
    #         ).date()
    #
    #     return None


class VerifySchema(BaseSchema):
    status: InvoiceVerifyAction
    remark: Optional[str] = Field(
        None, min_length=3, max_length=120, description="Add a valid remark")


class UpdateSchema(BaseSchema):
    status: InvoiceUpdateAction
    approval_date: Optional[date]
    payment_date: Optional[date]
    tax_percent: Optional[Decimal]
    tax: Optional[Decimal]
    file_url: Optional[str]
    remark: Optional[str] = Field(
        None, min_length=3, max_length=120, description="Add a valid remark")

