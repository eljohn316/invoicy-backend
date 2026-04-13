from typing import Annotated

from pydantic import BaseModel, Field, create_model
from pynanoid import generate

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
SIZE = 21


def generate_id():
    return generate(ALPHABET, SIZE)


def make_new_model(
    name: str, model_cls: type[BaseModel], fields: set | None = None
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
        name,
        __config__=model_cls.model_config,
        **new_fields,
    )
