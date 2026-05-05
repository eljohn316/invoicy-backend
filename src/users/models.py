from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from ..invoices import models


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
    invoices: Mapped[list[models.Invoice]] = relationship(back_populates="poster")

    @property
    def full_name(self) -> str:
        return self.first_name + " " + self.last_name
