from sqlalchemy import select

from ..dependencies import DatabaseDep
from . import models
from .schemas import InvoiceCreate, InvoiceUpdate


def get_invoices(db: DatabaseDep):
    result = db.execute(
        select(models.Invoice).order_by(models.Invoice.created_at.desc())
    )
    invoices = result.scalars().all()
    return invoices


def get_invoice(db: DatabaseDep, invoice_id: str):
    result = db.execute(select(models.Invoice).where(models.Invoice.id == invoice_id))
    invoice = result.scalars().first()
    return invoice


def create_invoice(db: DatabaseDep, invoice_data: InvoiceCreate):
    invoice_dict = invoice_data.model_dump(by_alias=False)
    new_invoice = models.Invoice(**invoice_dict)
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return new_invoice


def update_invoice(
    db: DatabaseDep,
    invoice: models.Invoice,
    invoice_data: InvoiceUpdate,
):
    invoice_dict = invoice_data.model_dump(by_alias=False, exclude_unset=True)
    for field, value in invoice_dict.items():
        setattr(invoice, field, value)
    db.commit()
    db.refresh(invoice)
    return invoice


def delete_invoice(db: DatabaseDep, invoice: models.Invoice):
    db.delete(invoice)
    db.commit()
