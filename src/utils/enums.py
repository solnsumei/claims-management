from enum import Enum


class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class InvoiceUpdateAction(str, Enum):
    Approved = "Approved"
    Paid = "Paid"
    Cancelled = "Cancelled"


class InvoiceStatus(InvoiceUpdateAction):
    New = "New"
    Pending = "Pending"


class Role(str, Enum):
    Admin = "Admin"
    Manager = "Manager"
    Staff = "Staff"
    Contractor = "Contractor"
