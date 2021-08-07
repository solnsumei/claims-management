from datetime import date
from pypika.terms import Parameter, Interval
from typing import Optional
from fastapi import Depends
from tortoise.query_utils import Q
from .baserouter import BaseRouter
from src.models import User, Claim, ClaimWithRelations
from src.utils.security import check_admin_or_manager
from src.utils.enums import InvoiceStatus, Role

router = BaseRouter()


@router.get("/")
async def get_reports(
        start_date: str,
        end_date: str,
        status: Optional[str] = None,
        auth: User = Depends(check_admin_or_manager)):

    filters = get_filters(status, auth)

    return await Claim.filter(**filters, created_at__gte=start_date, created_at__lte=end_date)


def get_filters(status, auth):
    filters = {}
    if auth.role == Role.Manager:
        filters['manager__id'] = auth.id

    if status != 'All':
        filters['status'] = status

    return filters
