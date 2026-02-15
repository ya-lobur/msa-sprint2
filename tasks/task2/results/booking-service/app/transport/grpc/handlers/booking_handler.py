"""gRPC handler for booking service."""
from typing import Callable

import structlog
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.manager.usecases import BookingUseCases
from app.infrastructure.repositories import BookingRepositorySA
from app.transport.grpc.generated import booking_pb2, booking_pb2_grpc

logger = structlog.get_logger()


class BookingServiceHandler(booking_pb2_grpc.BookingServiceServicer):
    """gRPC handler for booking service."""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        use_case_factory: Callable[[BookingRepositorySA], BookingUseCases],
    ):
        self.session_factory = session_factory
        self.use_case_factory = use_case_factory

    async def CreateBooking(self, request: booking_pb2.BookingRequest, context) -> booking_pb2.BookingResponse:
        """Handle CreateBooking gRPC request."""
        logger.info("create_booking_request", user_id=request.user_id, hotel_id=request.hotel_id)

        async with self.session_factory() as session:
            try:
                # Create repository with session
                repository = BookingRepositorySA(session)

                # Create use case with repository
                use_case = self.use_case_factory(repository)

                # Execute use case
                promo_code = request.promo_code if request.promo_code else None
                booking = await use_case.create_booking(request.user_id, request.hotel_id, promo_code)

                # Commit transaction
                await session.commit()

                # Convert to protobuf
                return booking_pb2.BookingResponse(
                    id=booking.id or "",
                    user_id=booking.user_id,
                    hotel_id=booking.hotel_id,
                    promo_code=booking.promo_code or "",
                    discount_percent=booking.discount_percent,
                    price=booking.price,
                    created_at=booking.created_at.isoformat() if booking.created_at else "",
                )
            except Exception:
                await session.rollback()
                raise

    async def ListBookings(self, request: booking_pb2.BookingListRequest, context) -> booking_pb2.BookingListResponse:
        """Handle ListBookings gRPC request."""
        user_id = request.user_id if request.user_id else None
        logger.info("list_bookings_request", user_id=user_id)

        async with self.session_factory() as session:
            try:
                # Create repository with session
                repository = BookingRepositorySA(session)

                # Create use case with repository
                use_case = self.use_case_factory(repository)

                # Execute use case
                bookings = await use_case.list_bookings(user_id)

                # Convert to protobuf
                responses = [
                    booking_pb2.BookingResponse(
                        id=booking.id or "",
                        user_id=booking.user_id,
                        hotel_id=booking.hotel_id,
                        promo_code=booking.promo_code or "",
                        discount_percent=booking.discount_percent,
                        price=booking.price,
                        created_at=booking.created_at.isoformat() if booking.created_at else "",
                    )
                    for booking in bookings
                ]

                return booking_pb2.BookingListResponse(bookings=responses)
            except Exception:
                await session.rollback()
                raise
