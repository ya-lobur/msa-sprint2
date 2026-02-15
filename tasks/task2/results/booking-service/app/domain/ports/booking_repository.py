"""Booking repository port."""
from abc import ABC, abstractmethod
from typing import List

from app.domain.entities import Booking


class BookingRepository(ABC):
    """Repository interface for bookings."""

    @abstractmethod
    async def save(self, booking: Booking) -> Booking:
        """Save a booking."""
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> List[Booking]:
        """Find bookings by user ID."""
        pass

    @abstractmethod
    async def find_all(self) -> List[Booking]:
        """Find all bookings."""
        pass
