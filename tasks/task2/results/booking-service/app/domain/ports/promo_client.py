"""Promo code service client port."""
from abc import ABC, abstractmethod
from typing import Optional


class PromoClient(ABC):
    """Client interface for promo code service."""

    @abstractmethod
    async def validate_promo(self, promo_code: str, user_id: str) -> Optional[float]:
        """Validate promo code and return discount amount, or None if invalid."""
        pass
