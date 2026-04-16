from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, computed_field
from pydantic.alias_generators import to_camel

from ..utils import make_new_model


class BaseSchemaModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_by_name=True,
        serialize_by_alias=True,
        alias_generator=to_camel,
    )


class Address(BaseSchemaModel):
    street: str
    city: str
    post_code: str
    country: str


class Item(BaseSchemaModel):
    name: str
    quantity: int
    price: float

    @computed_field
    @property
    def total(self) -> float:
        return self.quantity * self.price


class InvoiceBase(BaseSchemaModel):
    description: str
    payment_terms: int
    client_name: str
    client_email: EmailStr
    status: Literal["draft", "pending", "paid"]
    sender_address: Address
    client_address: Address
    items: list[Item]


class InvoiceOut(InvoiceBase):
    id: str
    created_at: datetime
    payment_due: datetime
    total: float


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(BaseSchemaModel):
    description: str | None = None
    payment_terms: int | None = None
    client_name: str | None = None
    client_email: EmailStr | None = None
    status: Literal["draft", "pending", "paid"] | None = None
    sender_address: Address | None = None
    client_address: Address | None = None
    items: list[Item] | None = None


InvoiceItem = make_new_model(
    "InvoiceItem",
    InvoiceOut,
    {
        "id",
        "created_at",
        "payment_due",
        "client_name",
        "status",
        "total",
    },
)
