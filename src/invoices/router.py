from fastapi import APIRouter, status

from ..dependencies import DatabaseDep
from .exceptions import InvoiceNotFound
from .schemas import InvoiceCreate, InvoiceItem, InvoiceOut
from .services import create_invoice, get_invoice, get_invoices

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.get("/", name="Get all invoices", response_model=list[InvoiceItem])
def get_invoices_handler(db: DatabaseDep):
    invoices = get_invoices(db)
    return invoices


@router.get("/{invoice_id}", name="Get invoice", response_model=InvoiceOut)
def get_invoice_handler(invoice_id: str, db: DatabaseDep):
    invoice = get_invoice(db, invoice_id)
    if invoice is None:
        raise InvoiceNotFound()
    return invoice


@router.post(
    "/",
    name="Create invoice",
    response_model=InvoiceOut,
    status_code=status.HTTP_201_CREATED,
)
def create_invoice_handler(invoice: InvoiceCreate, db: DatabaseDep):
    new_invoice = create_invoice(db, invoice)
    return new_invoice
