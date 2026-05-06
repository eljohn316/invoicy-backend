from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from ..auth import CurrentUserDep
from ..dependencies import DatabaseDep
from ..exceptions import ForbiddenException, NotFoundException
from .schemas import FilterParams, InvoiceCreate, InvoiceItem, InvoiceOut, InvoiceUpdate
from .services import InvoiceService

router = APIRouter(prefix="/invoices", tags=["invoices"])


def get_invoice_service(db: DatabaseDep):
    return InvoiceService(db)


InvoiceServiceDep = Annotated[InvoiceService, Depends(get_invoice_service)]


@router.get("/", name="Get all invoices", response_model=list[InvoiceItem])
async def get_invoices_handler(
    filter_query: Annotated[FilterParams, Query()],
    invoice_service: InvoiceServiceDep,
):
    invoices = await invoice_service.get_invoices(filter_query)
    return invoices


@router.get("/{invoice_id}", name="Get invoice", response_model=InvoiceOut)
async def get_invoice_handler(invoice_id: str, invoice_service: InvoiceServiceDep):
    invoice = await invoice_service.get_invoice(invoice_id)
    if invoice is None:
        raise NotFoundException(detail="Invoice not found")
    return invoice


@router.post(
    "/",
    name="Create invoice",
    response_model=InvoiceOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_invoice_handler(
    invoice_data: InvoiceCreate,
    current_user: CurrentUserDep,
    invoice_service: InvoiceServiceDep,
):
    new_invoice = await invoice_service.create_invoice(
        {**invoice_data.model_dump(by_alias=False), "poster_id": current_user.id}
    )
    return new_invoice


@router.patch(
    "/{invoice_id}",
    name="Update invoice",
    response_model=InvoiceOut,
)
async def update_invoice_handler(
    invoice_id: str,
    invoice_data: InvoiceUpdate,
    current_user: CurrentUserDep,
    invoice_service: InvoiceServiceDep,
):
    invoice = await invoice_service.get_invoice(invoice_id)

    if invoice is None:
        raise NotFoundException(detail="Invoice not found")

    if invoice.poster_id != current_user.id:
        raise ForbiddenException(
            detail="Not authorized to update this invoice",
        )

    updated_invoice = await invoice_service.update_invoice(invoice, invoice_data)
    return updated_invoice


@router.delete(
    "/{invoice_id}",
    name="Delete invoice",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_invoice_handler(
    invoice_id: str, current_user: CurrentUserDep, invoice_service: InvoiceServiceDep
):
    invoice = await invoice_service.get_invoice(invoice_id)

    if invoice is None:
        raise NotFoundException(detail="Invoice not found")

    if invoice.poster_id != current_user.id:
        raise ForbiddenException(detail="Not authorized to delete this invoice")

    await invoice_service.delete_invoice(invoice)
