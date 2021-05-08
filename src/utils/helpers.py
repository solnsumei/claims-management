from .enums import InvoiceStatus

updatable_statuses = [InvoiceStatus.Pending, InvoiceStatus.Initial_Approval, InvoiceStatus.Approved]
deletable_statuses = [InvoiceStatus.New, InvoiceStatus.Pending, InvoiceStatus.Cancelled]

upload_folder = "invoices"
