"""SQLAlchemy implementation of booking history repository."""
from typing import List

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import BookingHistory
from app.domain.ports import BookingHistoryRepository
from app.infrastructure.models import BookingHistoryModel

logger = structlog.get_logger()


class BookingHistoryRepositorySA(BookingHistoryRepository):
    """SQLAlchemy implementation of booking history repository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, booking_history: BookingHistory) -> BookingHistory:
        """Save booking history."""
        model = BookingHistoryModel(
            booking_id=booking_history.booking_id,
            user_id=booking_history.user_id,
            hotel_id=booking_history.hotel_id,
            promo_code=booking_history.promo_code,
            discount_percent=booking_history.discount_percent,
            price=booking_history.price,
            created_at=booking_history.created_at,
        )

        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)

        logger.info(
            "booking_history_saved",
            id=model.id,
            booking_id=model.booking_id,
            user_id=booking_history.user_id,
            hotel_id=booking_history.hotel_id,
        )

        return BookingHistory(
            id=model.id,
            booking_id=model.booking_id,
            user_id=model.user_id,
            hotel_id=model.hotel_id,
            promo_code=model.promo_code,
            discount_percent=model.discount_percent,
            price=model.price,
            created_at=model.created_at,
        )

    async def find_by_user_id(self, user_id: str) -> List[BookingHistory]:
        """Find booking history by user ID."""
        stmt = select(BookingHistoryModel).where(BookingHistoryModel.user_id == user_id)
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [
            BookingHistory(
                id=model.id,
                booking_id=model.booking_id,
                user_id=model.user_id,
                hotel_id=model.hotel_id,
                promo_code=model.promo_code,
                discount_percent=model.discount_percent,
                price=model.price,
                created_at=model.created_at,
            )
            for model in models
        ]

    async def find_all(self) -> List[BookingHistory]:
        """Find all booking history records."""
        stmt = select(BookingHistoryModel)
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [
            BookingHistory(
                id=model.id,
                booking_id=model.booking_id,
                user_id=model.user_id,
                hotel_id=model.hotel_id,
                promo_code=model.promo_code,
                discount_percent=model.discount_percent,
                price=model.price,
                created_at=model.created_at,
            )
            for model in models
        ]
