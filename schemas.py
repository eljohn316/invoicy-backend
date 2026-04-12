from datetime import datetime
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    computed_field,
    create_model,
)
from pydantic.alias_generators import to_camel


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


def make_new_model(
    model_name: str, model_cls: type[BaseModel], fields: set | None = None
) -> type[BaseModel]:
    new_fields = {}

    for f_name, f_info in model_cls.model_fields.items():
        if not fields or f_name not in fields:
            continue

        f_dct = f_info.asdict()
        new_fields[f_name] = (
            Annotated[
                f_dct.get("annotation"),
                *f_dct.get("metadata"),
                Field(**f_dct.get("attributes")),
            ],
            None,
        )

    return create_model(
        model_name,
        __config__=model_cls.model_config,
        **new_fields,
    )


InvoiceItem = make_new_model(
    "InvoiceItem",
    InvoiceOut,
    {
        "id",
        "created_at",
        "payment_due",
        "client_name",
        "status",
    },
)
