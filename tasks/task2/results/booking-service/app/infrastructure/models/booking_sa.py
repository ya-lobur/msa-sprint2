"""SQLAlchemy booking model."""
from datetime import datetime

from sqlalchemy import Float, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    pass


class BookingModel(Base):
    """SQLAlchemy model for bookings."""

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    hotel_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    promo_code: Mapped[str | None] = mapped_column(String, nullable=True)
    discount_percent: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
