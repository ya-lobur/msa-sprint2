"""HTTP implementation of hotel client."""
import structlog

from app.domain.ports import HotelClient
from .base import BaseHTTPClient

logger = structlog.get_logger()


class HotelClientHTTP(HotelClient):
    """HTTP client for hotel service."""

    def __init__(self, base_url: str, review_base_url: str):
        self.client = BaseHTTPClient(base_url)
        self.review_client = BaseHTTPClient(review_base_url)

    async def close(self):
        """Close HTTP clients."""
        await self.client.close()
        await self.review_client.close()

    async def is_hotel_operational(self, hotel_id: str) -> bool:
        """Check if hotel is operational."""
        try:
            result = await self.client.get(f"/api/hotels/{hotel_id}/operational")
            return bool(result) if isinstance(result, bool) else result == "true"
        except Exception as e:
            logger.error("hotel_operational_check_failed", hotel_id=hotel_id, error=str(e))
            return False

    async def is_hotel_fully_booked(self, hotel_id: str) -> bool:
        """Check if hotel is fully booked."""
        try:
            result = await self.client.get(f"/api/hotels/{hotel_id}/fully-booked")
            return bool(result) if isinstance(result, bool) else result == "true"
        except Exception as e:
            logger.error("hotel_fully_booked_check_failed", hotel_id=hotel_id, error=str(e))
            return False

    async def is_trusted_hotel(self, hotel_id: str) -> bool:
        """Check if hotel is trusted (based on reviews)."""
        try:
            result = await self.review_client.get(f"/api/reviews/hotel/{hotel_id}/trusted")
            return bool(result) if isinstance(result, bool) else result == "true"
        except Exception as e:
            logger.error("hotel_trusted_check_failed", hotel_id=hotel_id, error=str(e))
            return False
