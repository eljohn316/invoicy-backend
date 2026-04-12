from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import models
from data import invoices
from database import Base, engine, get_db
from schemas import InvoiceCreate, InvoiceItem, InvoiceOut

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/", include_in_schema=False)
def root():
    return {"message": "Hello from Invoice App API"}


@app.get("/api/invoices", response_model=list[InvoiceItem])
def get_invoices():
    return invoices


@app.get("/api/invoices/{invoice_id}", response_model=InvoiceOut)
def get_post(invoice_id: str):
    for invoice in invoices:
        if invoice.get("id") == invoice_id:
            return invoice
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found"
    )


@app.post(
    "/api/invoices",
    response_model=InvoiceOut,
    status_code=status.HTTP_201_CREATED,
)
def create_invoice(invoice: InvoiceCreate, db: Annotated[Session, Depends(get_db)]):
    new_invoice = models.Invoice(
        description=invoice.description,
        payment_terms=invoice.payment_terms,
        client_name=invoice.client_name,
        client_email=invoice.client_email,
        status=invoice.status,
        sender_address=invoice.sender_address.model_dump(),
        client_address=invoice.client_address.model_dump(),
        items=list(map(lambda item: item.model_dump(), invoice.items)),
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return new_invoice
