from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TypedDict

from sqlalchemy import JSON, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from ..users import models
from ..utils import generate_id

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
        String,
        primary_key=True,
        index=True,
        insert_default=generate_id,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    payment_terms: Mapped[int] = mapped_column(Integer, nullable=False)
    client_name: Mapped[str] = mapped_column(String, nullable=False)
    client_email: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    sender_address: Mapped[Address] = mapped_column(JSON, nullable=False)
    client_address: Mapped[Address] = mapped_column(JSON, nullable=False)
    items: Mapped[list[Item]] = mapped_column(JSON, nullable=False)
    date_issued: Mapped[datetime] = mapped_column(Date)
    poster_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    poster: Mapped[models.User] = relationship(back_populates="invoices")

    @property
    def total(self) -> float:
        items_total: int = 0
        for item in self.items:
            items_total += item["total"]
        return items_total

    @property
    def payment_due(self) -> datetime:
        return self.date_issued + timedelta(days=self.payment_terms)
