from enum import Enum


class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class InvoiceUpdateAction(str, Enum):
    Approved = "Approved"
    Paid = "Paid"
    Cancelled = "Cancelled"


class InvoiceStatus(str, Enum):
    New = "New"
    Pending = "Pending"
    Approved = "Approved"
    Paid = "Paid"
    Cancelled = "Cancelled"


class Role(str, Enum):
    Admin = "Admin"
    Manager = "Manager"
    Staff = "Staff"
    Contractor = "Contractor"


class EmployeeRole(str, Enum):
    Admin = "Admin"
    Manager = "Manager"
    Staff = "Staff"


class TeamAction(str, Enum):
    ADD = "add"
    REMOVE = "remove"
