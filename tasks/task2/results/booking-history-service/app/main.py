"""Main application entry point with composition root."""
import asyncio
import signal
from typing import Callable

import structlog

from app.common.logging import setup_logging
from app.infrastructure.db import create_engine, create_session_factory
from app.infrastructure.messaging import EventHandler, KafkaConsumer
from app.infrastructure.repositories import BookingHistoryRepositorySA
from app.manager.usecases import BookingHistoryUseCases
from app.settings import get_settings

logger = structlog.get_logger()


def create_use_case_factory() -> Callable[[BookingHistoryRepositorySA], BookingHistoryUseCases]:
    """Create factory for booking history use cases."""

    def factory(repository: BookingHistoryRepositorySA) -> BookingHistoryUseCases:
        return BookingHistoryUseCases(booking_history_repository=repository)

    return factory


async def serve():
    """Start Kafka consumer service."""
    settings = get_settings()

    # Setup logging
    setup_logging(settings.log_level)
    logger.info("starting_booking_history_service")

    # Create database engine and session factory
    engine = create_engine(settings.database_url)
    session_factory = create_session_factory(engine)

    # Create use case factory
    use_case_factory = create_use_case_factory()

    # Create event handler
    event_handler = EventHandler(session_factory, use_case_factory)

    # Create Kafka consumer
    kafka_consumer = KafkaConsumer(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        topic=settings.kafka_topic,
        group_id=settings.kafka_group_id,
        message_handler=event_handler.handle_message,
    )

    await kafka_consumer.start()

    # Setup signal handlers
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def signal_handler(sig, frame):
        logger.info("received_shutdown_signal", signal=sig)
        loop.call_soon_threadsafe(stop_event.set)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start consuming in a task
    consume_task = asyncio.create_task(kafka_consumer.consume())

    logger.info("service_started", topic=settings.kafka_topic, group_id=settings.kafka_group_id)

    # Wait for shutdown signal
    await stop_event.wait()

    # Graceful shutdown
    logger.info("shutting_down_service")
    await kafka_consumer.stop()

    # Wait for consume task to finish
    try:
        await asyncio.wait_for(consume_task, timeout=5.0)
    except asyncio.TimeoutError:
        logger.warning("consume_task_timeout")
        consume_task.cancel()

    await engine.dispose()
    logger.info("service_shutdown_complete")


def main():
    """Main entry point."""
    asyncio.run(serve())


if __name__ == "__main__":
    main()
