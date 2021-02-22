from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import Field, UUID4
from .baseschema import BaseSchema, DescriptionSchema
from src.utils.enums import InvoiceUpdateAction


class CreateSchema(DescriptionSchema):
    invoice_no: str = Field(..., min_length=2, max_length=15)
    title: str = Field(..., min_length=3, max_length=70, description="Title is required")
    amount: Decimal = Field(..., gt=0)
    duration: int = Field(..., gt=0)
    department_id: Optional[UUID4]
    project_id: Optional[UUID4]
    due_date: Optional[date]


class UpdateSchema(BaseSchema):
    status: InvoiceUpdateAction
    payment_date: Optional[date]
    remark: Optional[str] = Field(
        None, min_length=3, max_length=120, description="Add a valid remark")
