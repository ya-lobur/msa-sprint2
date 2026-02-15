"""BookingCreated event model."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class BookingCreated(BaseModel):
    """BookingCreated event."""

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()}
    )

    id: str = Field(..., description="Booking ID")
    user_id: str = Field(..., description="User ID")
    hotel_id: str = Field(..., description="Hotel ID")
    price: float = Field(..., description="Final price after discount")
    promo_code: Optional[str] = Field(None, description="Promo code used")
    discount_percent: float = Field(default=0.0, description="Discount percentage applied")
    created_at: datetime = Field(..., description="Booking creation timestamp")
