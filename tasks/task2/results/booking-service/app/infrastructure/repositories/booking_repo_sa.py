"""SQLAlchemy implementation of booking repository."""
from typing import List

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.time import utcnow
from app.domain.entities import Booking
from app.domain.ports import BookingRepository
from app.infrastructure.models import BookingModel

logger = structlog.get_logger()


class BookingRepositorySA(BookingRepository):
    """SQLAlchemy implementation of booking repository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, booking: Booking) -> Booking:
        """Save a booking."""
        model = BookingModel(
            user_id=booking.user_id,
            hotel_id=booking.hotel_id,
            promo_code=booking.promo_code,
            discount_percent=booking.discount_percent,
            price=booking.price,
            created_at=utcnow(),
        )

        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)

        logger.info("booking_saved", booking_id=model.id, user_id=booking.user_id, hotel_id=booking.hotel_id)

        return Booking(
            id=str(model.id),
            user_id=model.user_id,
            hotel_id=model.hotel_id,
            promo_code=model.promo_code,
            discount_percent=model.discount_percent,
            price=model.price,
            created_at=model.created_at,
        )

    async def find_by_user_id(self, user_id: str) -> List[Booking]:
        """Find bookings by user ID."""
        stmt = select(BookingModel).where(BookingModel.user_id == user_id)
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [
            Booking(
                id=str(model.id),
                user_id=model.user_id,
                hotel_id=model.hotel_id,
                promo_code=model.promo_code,
                discount_percent=model.discount_percent,
                price=model.price,
                created_at=model.created_at,
            )
            for model in models
        ]

    async def find_all(self) -> List[Booking]:
        """Find all bookings."""
        stmt = select(BookingModel)
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [
            Booking(
                id=str(model.id),
                user_id=model.user_id,
                hotel_id=model.hotel_id,
                promo_code=model.promo_code,
                discount_percent=model.discount_percent,
                price=model.price,
                created_at=model.created_at,
            )
            for model in models
        ]
