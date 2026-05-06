from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .. import models
from .schemas import FilterParams, InvoiceUpdate


class InvoiceService:
    def __init__(self, db_session: AsyncSession):
        self._db = db_session

    async def get_invoices(self, filter_query: FilterParams):
        query = select(models.Invoice).order_by(models.Invoice.created_at.desc())

        if len(filter_query.status) >= 1:
            query = query.where(models.Invoice.status.in_(filter_query.status))

        result = await self._db.execute(query)
        invoices = result.scalars().all()

        return invoices

    async def get_invoice(self, invoice_id: str):
        result = await self._db.execute(
            select(models.Invoice)
            .options(selectinload(models.Invoice.poster))
            .where(models.Invoice.id == invoice_id)
        )
        invoice = result.scalars().first()
        return invoice

    async def create_invoice(self, invoice_data: dict[str, Any]):
        new_invoice = models.Invoice(**invoice_data)
        self._db.add(new_invoice)
        await self._db.commit()
        await self._db.refresh(new_invoice)
        return new_invoice

    async def update_invoice(
        self,
        invoice: models.Invoice,
        invoice_data: InvoiceUpdate,
    ):
        invoice_dict = invoice_data.model_dump(by_alias=False, exclude_unset=True)
        for field, value in invoice_dict.items():
            setattr(invoice, field, value)
        await self._db.commit()
        await self._db.refresh(invoice)
        return invoice

    async def delete_invoice(self, invoice: models.Invoice):
        await self._db.delete(invoice)
        await self._db.commit()
