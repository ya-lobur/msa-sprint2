"""Booking history use cases."""
from datetime import datetime

import structlog

from app.domain.entities import BookingHistory
from app.domain.events import BookingCreated
from app.domain.ports import BookingHistoryRepository

logger = structlog.get_logger()


class BookingHistoryUseCases:
    """Use cases for booking history."""

    def __init__(self, booking_history_repository: BookingHistoryRepository):
        self.booking_history_repository = booking_history_repository

    async def process_booking_created(self, event: BookingCreated) -> BookingHistory:
        """Process BookingCreated event and save to history.

        Args:
            event: BookingCreated event

        Returns:
            Saved booking history
        """
        logger.info(
            "processing_booking_created_event",
            booking_id=event.id,
            user_id=event.user_id,
            hotel_id=event.hotel_id,
        )

        # Create booking history entity
        booking_history = BookingHistory(
            booking_id=event.id,
            user_id=event.user_id,
            hotel_id=event.hotel_id,
            price=event.price,
            promo_code=event.promo_code,
            discount_percent=event.discount_percent,
            created_at=event.created_at,
        )

        # Save to repository
        saved_history = await self.booking_history_repository.save(booking_history)

        logger.info(
            "booking_history_created",
            id=saved_history.id,
            booking_id=saved_history.booking_id,
            user_id=saved_history.user_id,
        )

        return saved_history
