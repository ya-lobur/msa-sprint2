"""Main application entry point with composition root."""
import asyncio
import signal
from typing import Callable

import grpc
# from grpc_reflection.v1alpha import reflection
import structlog

from app.manager.usecases import BookingUseCases
from app.common.logging import setup_logging
from app.domain.services import PricingService
from app.infrastructure.clients.http import HotelClientHTTP, PromoClientHTTP, UserClientHTTP
from app.infrastructure.db import create_engine, create_session_factory
from app.infrastructure.repositories import BookingRepositorySA
from app.settings import get_settings
from app.transport.grpc.handlers import BookingServiceHandler
from app.transport.grpc.interceptors import ErrorMappingInterceptor, LoggingInterceptor

# Import generated gRPC code
from app.transport.grpc.generated import booking_pb2, booking_pb2_grpc

logger = structlog.get_logger()


def create_use_case_factory(
    user_client: UserClientHTTP,
    hotel_client: HotelClientHTTP,
    promo_client: PromoClientHTTP,
    pricing_service: PricingService,
) -> Callable[[BookingRepositorySA], BookingUseCases]:
    """Create factory for booking use cases."""

    def factory(repository: BookingRepositorySA) -> BookingUseCases:
        return BookingUseCases(
            booking_repository=repository,
            user_client=user_client,
            hotel_client=hotel_client,
            promo_client=promo_client,
            pricing_service=pricing_service,
        )

    return factory


async def serve():
    """Start gRPC server."""
    settings = get_settings()

    # Setup logging
    setup_logging(settings.log_level)
    logger.info("starting_booking_service", grpc_host=settings.grpc_host, grpc_port=settings.grpc_port)

    # Create database engine and session factory
    engine = create_engine(settings.database_url)
    session_factory = create_session_factory(engine)

    # Create HTTP clients
    user_client = UserClientHTTP(settings.user_service_url)
    hotel_client = HotelClientHTTP(settings.hotel_service_url, settings.review_service_url)
    promo_client = PromoClientHTTP(settings.promo_service_url)

    # Create domain services
    pricing_service = PricingService()

    # Create use case factory
    use_case_factory = create_use_case_factory(user_client, hotel_client, promo_client, pricing_service)

    # Create gRPC server with interceptors
    server = grpc.aio.server(
        interceptors=[
            LoggingInterceptor(),
            ErrorMappingInterceptor(),
        ]
    )

    # Create and register handler
    handler = BookingServiceHandler(session_factory, use_case_factory)
    booking_pb2_grpc.add_BookingServiceServicer_to_server(handler, server)

    # Enable reflection
    # service_names = (
    #     booking_pb2.DESCRIPTOR.services_by_name['BookingService'].full_name,
    #     reflection.SERVICE_NAME,
    # )
    # reflection.enable_server_reflection(service_names, server)

    # Bind server
    listen_addr = f"{settings.grpc_host}:{settings.grpc_port}"
    server.add_insecure_port(listen_addr)

    # Start server
    await server.start()
    logger.info("grpc_server_started", address=listen_addr)

    # Setup signal handlers
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def signal_handler(sig, frame):
        logger.info("received_shutdown_signal", signal=sig)
        loop.call_soon_threadsafe(stop_event.set)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Wait for shutdown signal
    await stop_event.wait()

    # Graceful shutdown
    logger.info("shutting_down_server")
    await server.stop(grace=5)
    await user_client.close()
    await hotel_client.close()
    await promo_client.close()
    await engine.dispose()
    logger.info("server_shutdown_complete")


def main():
    """Main entry point."""
    asyncio.run(serve())


if __name__ == "__main__":
    main()
