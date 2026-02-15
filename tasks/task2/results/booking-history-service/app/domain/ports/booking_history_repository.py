"""Booking history repository port."""
from abc import ABC, abstractmethod
from typing import List

from app.domain.entities import BookingHistory


class BookingHistoryRepository(ABC):
    """Repository interface for booking history."""

    @abstractmethod
    async def save(self, booking_history: BookingHistory) -> BookingHistory:
        """Save booking history."""
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> List[BookingHistory]:
        """Find booking history by user ID."""
        pass

    @abstractmethod
    async def find_all(self) -> List[BookingHistory]:
        """Find all booking history records."""
        pass
