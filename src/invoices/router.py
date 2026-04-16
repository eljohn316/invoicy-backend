from typing import Annotated

from fastapi import APIRouter, Query, status

from ..dependencies import DatabaseDep
from .exceptions import InvoiceNotFound
from .schemas import FilterParams, InvoiceCreate, InvoiceItem, InvoiceOut, InvoiceUpdate
from .services import (
    create_invoice,
    delete_invoice,
    get_invoice,
    get_invoices,
    update_invoice,
)

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.get("/", name="Get all invoices", response_model=list[InvoiceItem])
async def get_invoices_handler(
    filter_query: Annotated[FilterParams, Query()],
    db: DatabaseDep,
):
    invoices = await get_invoices(db, filter_query)
    return invoices


@router.get("/{invoice_id}", name="Get invoice", response_model=InvoiceOut)
async def get_invoice_handler(invoice_id: str, db: DatabaseDep):
    invoice = await get_invoice(db, invoice_id)
    if invoice is None:
        raise InvoiceNotFound()
    return invoice


@router.post(
    "/",
    name="Create invoice",
    response_model=InvoiceOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_invoice_handler(invoice_data: InvoiceCreate, db: DatabaseDep):
    new_invoice = await create_invoice(db, invoice_data)
    return new_invoice


@router.patch(
    "/{invoice_id}",
    name="Update invoice",
    response_model=InvoiceOut,
)
async def update_invoice_handler(
    invoice_id: str,
    invoice_data: InvoiceUpdate,
    db: DatabaseDep,
):
    invoice = await get_invoice(db, invoice_id)
    if invoice is None:
        raise InvoiceNotFound()
    updated_invoice = await update_invoice(db, invoice, invoice_data)
    return updated_invoice


@router.delete(
    "/{invoice_id}",
    name="Delete invoice",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_invoice_handler(invoice_id: str, db: DatabaseDep):
    invoice = await get_invoice(db, invoice_id)
    if invoice is None:
        raise InvoiceNotFound()
    await delete_invoice(db, invoice)
