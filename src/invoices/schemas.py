from datetime import date, datetime
from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, EmailStr, Field, computed_field
from pydantic.alias_generators import to_camel

from ..utils import make_new_model


class FilterParams(BaseModel):
    model_config = ConfigDict(extra="ignore")

    status: list[str] = []


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
    client_email: Union[Literal[""], EmailStr] = Field(union_mode="left_to_right")
    status: Literal["draft", "pending", "paid"]
    sender_address: Address
    client_address: Address
    items: list[Item]
    date_issued: date = Field(default_factory=lambda: date.today())


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
    date_issued: date | None = None


InvoiceItem = make_new_model(
    "InvoiceItem",
    InvoiceOut,
    {
        "id",
        "payment_due",
        "client_name",
        "status",
        "total",
    },
)
