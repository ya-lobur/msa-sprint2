"""Kafka consumer for consuming events."""
import json
from typing import Callable, Awaitable

import structlog
from aiokafka import AIOKafkaConsumer

logger = structlog.get_logger()


class KafkaConsumer:
    """Kafka consumer wrapper."""

    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
        group_id: str,
        message_handler: Callable[[dict], Awaitable[None]],
    ):
        """Initialize Kafka consumer.

        Args:
            bootstrap_servers: Kafka bootstrap servers
            topic: Topic name to consume from
            group_id: Consumer group ID
            message_handler: Async function to handle messages
        """
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.message_handler = message_handler
        self.consumer: AIOKafkaConsumer | None = None
        self._running = False

    async def start(self) -> None:
        """Start Kafka consumer."""
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
        await self.consumer.start()
        logger.info(
            "kafka_consumer_started",
            bootstrap_servers=self.bootstrap_servers,
            topic=self.topic,
            group_id=self.group_id,
        )

    async def stop(self) -> None:
        """Stop Kafka consumer."""
        self._running = False
        if self.consumer:
            await self.consumer.stop()
            logger.info("kafka_consumer_stopped")

    async def consume(self) -> None:
        """Consume messages from Kafka topic."""
        if not self.consumer:
            raise RuntimeError("Kafka consumer not started")

        self._running = True
        logger.info("kafka_consumer_consuming", topic=self.topic)

        try:
            async for message in self.consumer:
                if not self._running:
                    break

                try:
                    logger.info(
                        "message_received",
                        topic=message.topic,
                        partition=message.partition,
                        offset=message.offset,
                    )

                    # Handle message
                    await self.message_handler(message.value)

                except Exception as e:
                    logger.error(
                        "message_processing_failed",
                        topic=message.topic,
                        offset=message.offset,
                        error=str(e),
                        exc_info=True,
                    )
                    # Continue processing other messages
                    continue

        except Exception as e:
            logger.error("kafka_consumer_error", error=str(e), exc_info=True)
            raise
