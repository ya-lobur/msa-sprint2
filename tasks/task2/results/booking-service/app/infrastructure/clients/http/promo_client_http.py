"""HTTP implementation of promo client."""
from typing import Optional

import structlog

from app.domain.ports import PromoClient
from .base import BaseHTTPClient

logger = structlog.get_logger()


class PromoClientHTTP(PromoClient):
    """HTTP client for promo code service."""

    def __init__(self, base_url: str):
        self.client = BaseHTTPClient(base_url)

    async def close(self):
        """Close HTTP client."""
        await self.client.close()

    async def validate_promo(self, promo_code: str, user_id: str) -> Optional[float]:
        """Validate promo code and return discount amount."""
        try:
            result = await self.client.post(f"/api/promos/validate?code={promo_code}&userId={user_id}")

            if isinstance(result, dict) and "discount" in result:
                return float(result["discount"])

            logger.warning("promo_validation_no_discount", promo_code=promo_code, user_id=user_id)
            return None

        except Exception as e:
            logger.error("promo_validation_failed", promo_code=promo_code, user_id=user_id, error=str(e))
            return None
