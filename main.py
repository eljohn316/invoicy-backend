from fastapi import FastAPI, HTTPException, status

from data import invoices
from schemas import InvoiceIn, InvoiceOut, InvoiceItem


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


@app.post("/api/invoices", response_model=InvoiceOut)
def create_invoice(invoice: InvoiceIn):
    return invoice
