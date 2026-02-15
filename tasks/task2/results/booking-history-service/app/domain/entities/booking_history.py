"""Booking history domain entity."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class BookingHistory:
    """Booking history domain entity."""

    booking_id: str
    user_id: str
    hotel_id: str
    price: float
    promo_code: Optional[str] = None
    discount_percent: float = 0.0
    created_at: Optional[datetime] = None
    id: Optional[int] = None
