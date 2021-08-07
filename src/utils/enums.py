from enum import Enum


class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class InvoiceUpdateAction(str, Enum):
    Approved = "Approved"
    Paid = "Paid"
    Cancelled = "Cancelled"


class InvoiceVerifyAction(str, Enum):
    Verified = "Verified"
    Cancelled = "Cancelled"


class InvoiceStatus(str, Enum):
    New = "New"
    Pending = "Pending"
    Verified = "Verified"
    Approved = "Approved"
    Paid = "Paid"
    Cancelled = "Cancelled"


class Role(str, Enum):
    Admin = "Admin"
    Manager = "Manager"
    Staff = "Staff"
    Contractor = "Contractor"


class StaffRole(str, Enum):
    Staff = "Staff"


class EmployeeRole(str, Enum):
    Admin = "Admin"
    Manager = "Manager"
    Staff = "Staff"


class TeamAction(str, Enum):
    ADD = "add"
    REMOVE = "remove"
