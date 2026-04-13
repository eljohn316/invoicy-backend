from fastapi import HTTPException, status


class InvoiceNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found"
        )
