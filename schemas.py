from datetime import datetime
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    create_model,
    computed_field,
    EmailStr,
)
from pydantic.alias_generators import to_camel


class BaseSchemaModel(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True, serialize_by_alias=True, alias_generator=to_camel
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
    payment_due: datetime
    description: str
    payment_terms: int
    client_name: str
    client_email: EmailStr
    status: Literal["draft", "pending", "paid"]
    sender_address: Address
    client_address: Address
    items: list[Item] = Field(default_factory=list)

    @computed_field
    @property
    def total(self) -> float:
        if len(self.items) == 0:
            return 0
        return sum([item.total for item in self.items])


class InvoiceOut(InvoiceBase):
    id: str
    created_at: datetime


class InvoiceIn(InvoiceBase):
    pass


def make_new_model(
    model_name: str, model_cls: type[BaseModel], fields: set | None = None
) -> type[BaseModel]:
    new_fields = {}

    for f_name, f_info in model_cls.model_fields.items():
        if not fields or not f_name in fields:
            continue

        f_dct = f_info.asdict()
        new_fields[f_name] = (
            Annotated[
                f_dct["annotation"],
                *f_dct["metadata"],
                Field(**f_dct["attributes"]),
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
