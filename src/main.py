from fastapi import FastAPI

from src.database import Base, engine
from src.invoices.router import router as invoice_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Invoices App API", root_path="/api")


app.include_router(invoice_router)
