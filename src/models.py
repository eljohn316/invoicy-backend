from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TypedDict

from pynanoid import generate
from sqlalchemy import JSON, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def generate_id():
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
    SIZE = 21
    return generate(ALPHABET, SIZE)


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


class Base(DeclarativeBase):
    pass


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
    poster: Mapped[User] = relationship(back_populates="invoices")

    @property
    def total(self) -> float:
        items_total: int = 0
        for item in self.items:
            items_total += item["total"]
        return items_total

    @property
    def payment_due(self) -> datetime:
        return self.date_issued + timedelta(days=self.payment_terms)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    profile_image: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        default=None,
    )
    invoices: Mapped[list[Invoice]] = relationship(back_populates="poster")

    @property
    def full_name(self) -> str:
        return self.first_name + " " + self.last_name
