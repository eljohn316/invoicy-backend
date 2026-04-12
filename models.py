from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TypedDict

from pynanoid import generate
from sqlalchemy import JSON, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


def generate_id():
    return generate("0123456789abcdefghijklmnopqrstuvwxyz", size=21)


Address = TypedDict(
    "Address",
    {
        "street": str,
        "city": str,
        "post_code": str,
        "country": str,
    },
)

Item = TypedDict(
    "Item",
    {"name": str, "quantity": int, "price": float, "total": float},
)


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, index=True, insert_default=generate_id
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    payment_terms: Mapped[int] = mapped_column(Integer, nullable=False)
    client_name: Mapped[str] = mapped_column(String, nullable=False)
    client_email: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    sender_address: Mapped[Address] = mapped_column(JSON, nullable=False)
    client_address: Mapped[Address] = mapped_column(JSON, nullable=False)
    items: Mapped[Item] = mapped_column(JSON, nullable=False)

    @property
    def total(self) -> float:
        print(self.items)
        items_total: int = 0
        for item in self.items:
            items_total += item["total"]
        return items_total

    @property
    def payment_due(self) -> datetime:
        return self.created_at + timedelta(days=self.payment_terms)
