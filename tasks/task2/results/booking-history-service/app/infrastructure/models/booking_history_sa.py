"""SQLAlchemy booking history model."""
from datetime import datetime

from sqlalchemy import Float, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    pass


class BookingHistoryModel(Base):
    """SQLAlchemy model for booking history."""

    __tablename__ = "booking_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    booking_id: Mapped[str] = mapped_column(String, nullable=False, index=True, unique=True)
    user_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    hotel_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    promo_code: Mapped[str | None] = mapped_column(String, nullable=True)
    discount_percent: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
