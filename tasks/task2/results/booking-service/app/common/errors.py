"""Domain exceptions and error handling."""


class BookingError(Exception):
    """Base exception for booking errors."""

    pass


class UserValidationError(BookingError):
    """User validation failed."""

    pass


class HotelValidationError(BookingError):
    """Hotel validation failed."""

    pass


class PromoValidationError(BookingError):
    """Promo code validation failed."""

    pass
