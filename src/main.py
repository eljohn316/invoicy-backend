from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import Base, engine
from src.invoices.router import router as invoice_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="Invoices App API", root_path="/api", lifespan=lifespan)


app.include_router(invoice_router)
