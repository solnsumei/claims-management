from datetime import datetime
from .enums import InvoiceStatus


updatable_statuses = [InvoiceStatus.Pending, InvoiceStatus.Verified, InvoiceStatus.Approved]
deletable_statuses = [InvoiceStatus.New, InvoiceStatus.Pending, InvoiceStatus.Cancelled]

upload_folder = "invoices"


def get_claim_folder(date):
    return f"{date.strftime('%Y/%b')}"


def get_date(date_str: str):
    pass


def get_filters(start=None, end=None, status=None):
    pass
