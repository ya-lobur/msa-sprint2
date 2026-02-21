"""Booking domain entity."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Booking:
    """Booking domain entity."""

    user_id: str
    hotel_id: str
    price: float
    promo_code: Optional[str] = None
    discount_percent: float = 0.0
    id: Optional[str] = None
    created_at: Optional[datetime] = None
