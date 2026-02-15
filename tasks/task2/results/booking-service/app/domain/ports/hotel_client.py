"""Hotel service client port."""
from abc import ABC, abstractmethod


class HotelClient(ABC):
    """Client interface for hotel service."""

    @abstractmethod
    async def is_hotel_operational(self, hotel_id: str) -> bool:
        """Check if hotel is operational."""
        pass

    @abstractmethod
    async def is_hotel_fully_booked(self, hotel_id: str) -> bool:
        """Check if hotel is fully booked."""
        pass

    @abstractmethod
    async def is_trusted_hotel(self, hotel_id: str) -> bool:
        """Check if hotel is trusted (based on reviews)."""
        pass
