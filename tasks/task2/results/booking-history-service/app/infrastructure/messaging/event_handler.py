"""Event handler for processing Kafka messages."""
from datetime import datetime
from typing import Callable

import structlog
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.domain.events import BookingCreated
from app.infrastructure.repositories import BookingHistoryRepositorySA
from app.manager.usecases import BookingHistoryUseCases

logger = structlog.get_logger()


class EventHandler:
    """Handler for processing incoming Kafka events."""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        use_case_factory: Callable[[BookingHistoryRepositorySA], BookingHistoryUseCases],
    ):
        """Initialize event handler.

        Args:
            session_factory: Database session factory
            use_case_factory: Factory for creating use cases
        """
        self.session_factory = session_factory
        self.use_case_factory = use_case_factory

    async def handle_message(self, message: dict) -> None:
        """Handle incoming Kafka message.

        Args:
            message: Message dictionary with event_type and data
        """
        event_type = message.get("event_type")
        data = message.get("data")

        if event_type != "BookingCreated":
            logger.warning("unknown_event_type", event_type=event_type)
            return

        logger.info("processing_event", event_type=event_type, data=data)

        # Parse event data
        try:
            # Convert ISO format string to datetime if needed
            if isinstance(data.get("created_at"), str):
                data["created_at"] = datetime.fromisoformat(data["created_at"])

            event = BookingCreated(**data)
        except Exception as e:
            logger.error("event_parsing_failed", error=str(e), data=data, exc_info=True)
            raise

        # Process event
        async with self.session_factory() as session:
            try:
                repository = BookingHistoryRepositorySA(session)
                use_case = self.use_case_factory(repository)

                await use_case.process_booking_created(event)
                await session.commit()

                logger.info("event_processed_successfully", event_type=event_type, booking_id=event.id)
            except Exception as e:
                await session.rollback()
                logger.error(
                    "event_processing_failed",
                    event_type=event_type,
                    booking_id=data.get("id"),
                    error=str(e),
                    exc_info=True,
                )
                raise
