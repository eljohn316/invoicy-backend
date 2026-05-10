from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import settings
from src.database import engine
from src.invoices.router import router as invoice_router
from src.users.router import router as user_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(title="Invoices App API", root_path="/api", lifespan=lifespan)


if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(invoice_router)
app.include_router(user_router)


@app.get("/utils/health-check", tags=["utils"])
async def health_check() -> bool:
    return True


@app.exception_handler(ResponseValidationError)
async def response_validation_exception_handler(
    request: Request,
    exc: ResponseValidationError,
):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
