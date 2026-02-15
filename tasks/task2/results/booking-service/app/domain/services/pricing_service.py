"""Pricing service for booking calculations."""
import structlog

logger = structlog.get_logger()


class PricingService:
    """Service for calculating booking prices."""

    VIP_BASE_PRICE = 80.0
    STANDARD_BASE_PRICE = 100.0

    def calculate_base_price(self, user_status: str | None) -> float:
        """Calculate base price based on user status."""
        if user_status and user_status.upper() == "VIP":
            logger.debug("vip_user_pricing", user_status=user_status, base_price=self.VIP_BASE_PRICE)
            return self.VIP_BASE_PRICE

        logger.debug("standard_user_pricing", user_status=user_status, base_price=self.STANDARD_BASE_PRICE)
        return self.STANDARD_BASE_PRICE

    def calculate_final_price(self, base_price: float, discount: float) -> float:
        """Calculate final price after applying discount."""
        final_price = base_price - discount
        logger.debug("price_calculated", base_price=base_price, discount=discount, final_price=final_price)
        return final_price
