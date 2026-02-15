"""Booking use cases orchestration."""
from typing import List, Optional

import structlog

from app.common.errors import HotelValidationError, UserValidationError
from app.domain.entities import Booking
from app.domain.ports import BookingRepository, HotelClient, PromoClient, UserClient
from app.domain.services import PricingService

logger = structlog.get_logger()


class BookingUseCases:
    """Use cases for booking operations."""

    def __init__(
        self,
        booking_repository: BookingRepository,
        user_client: UserClient,
        hotel_client: HotelClient,
        promo_client: PromoClient,
        pricing_service: PricingService,
    ):
        self.booking_repository = booking_repository
        self.user_client = user_client
        self.hotel_client = hotel_client
        self.promo_client = promo_client
        self.pricing_service = pricing_service

    async def create_booking(self, user_id: str, hotel_id: str, promo_code: Optional[str] = None) -> Booking:
        """Create a new booking."""
        logger.info("creating_booking", user_id=user_id, hotel_id=hotel_id, promo_code=promo_code)

        # Validate user
        await self._validate_user(user_id)

        # Validate hotel
        await self._validate_hotel(hotel_id)

        # Calculate pricing
        user_status = await self.user_client.get_user_status(user_id)
        base_price = self.pricing_service.calculate_base_price(user_status)

        # Apply promo discount if provided
        discount = 0.0
        if promo_code:
            promo_discount = await self.promo_client.validate_promo(promo_code, user_id)
            if promo_discount:
                discount = promo_discount
                logger.info("promo_applied", promo_code=promo_code, discount=discount)
            else:
                logger.warning("promo_invalid", promo_code=promo_code, user_id=user_id)

        final_price = self.pricing_service.calculate_final_price(base_price, discount)

        # Create booking entity
        booking = Booking(
            user_id=user_id,
            hotel_id=hotel_id,
            promo_code=promo_code,
            discount_percent=discount,
            price=final_price,
        )

        # Save booking
        saved_booking = await self.booking_repository.save(booking)
        logger.info("booking_created", booking_id=saved_booking.id, price=final_price)

        return saved_booking

    async def list_bookings(self, user_id: Optional[str] = None) -> List[Booking]:
        """List bookings, optionally filtered by user ID."""
        if user_id:
            logger.debug("listing_bookings_by_user", user_id=user_id)
            return await self.booking_repository.find_by_user_id(user_id)
        else:
            logger.debug("listing_all_bookings")
            return await self.booking_repository.find_all()

    async def _validate_user(self, user_id: str) -> None:
        """Validate user eligibility for booking."""
        is_active = await self.user_client.is_user_active(user_id)
        if not is_active:
            logger.warning("user_inactive", user_id=user_id)
            raise UserValidationError("User is inactive")

        is_blacklisted = await self.user_client.is_user_blacklisted(user_id)
        if is_blacklisted:
            logger.warning("user_blacklisted", user_id=user_id)
            raise UserValidationError("User is blacklisted")

    async def _validate_hotel(self, hotel_id: str) -> None:
        """Validate hotel availability for booking."""
        is_operational = await self.hotel_client.is_hotel_operational(hotel_id)
        if not is_operational:
            logger.warning("hotel_not_operational", hotel_id=hotel_id)
            raise HotelValidationError("Hotel is not operational")

        is_trusted = await self.hotel_client.is_trusted_hotel(hotel_id)
        if not is_trusted:
            logger.warning("hotel_not_trusted", hotel_id=hotel_id)
            raise HotelValidationError("Hotel is not trusted based on reviews")

        is_fully_booked = await self.hotel_client.is_hotel_fully_booked(hotel_id)
        if is_fully_booked:
            logger.warning("hotel_fully_booked", hotel_id=hotel_id)
            raise HotelValidationError("Hotel is fully booked")
