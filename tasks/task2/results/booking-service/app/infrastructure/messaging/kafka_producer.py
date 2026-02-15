"""Kafka producer for publishing events."""
import json

import structlog
from aiokafka import AIOKafkaProducer
from pydantic import BaseModel

logger = structlog.get_logger()


class KafkaProducer:
    """Kafka producer wrapper."""

    def __init__(self, bootstrap_servers: str, topic: str):
        """Initialize Kafka producer.

        Args:
            bootstrap_servers: Kafka bootstrap servers
            topic: Default topic name
        """
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer: AIOKafkaProducer | None = None

    async def start(self) -> None:
        """Start Kafka producer."""
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await self.producer.start()
        logger.info("kafka_producer_started", bootstrap_servers=self.bootstrap_servers)

    async def stop(self) -> None:
        """Stop Kafka producer."""
        if self.producer:
            await self.producer.stop()
            logger.info("kafka_producer_stopped")

    async def publish(self, event: BaseModel, event_name: str) -> None:
        """Publish event to Kafka.

        Args:
            event: Event data (Pydantic model)
            event_name: Event name/type
        """
        if not self.producer:
            raise RuntimeError("Kafka producer not started")

        # Serialize event to dict
        event_dict = event.model_dump(mode="json")

        # Add event metadata
        message = {
            "event_type": event_name,
            "data": event_dict,
        }

        try:
            await self.producer.send_and_wait(self.topic, value=message)
            logger.info(
                "event_published",
                event_type=event_name,
                topic=self.topic,
            )
        except Exception as e:
            logger.error(
                "event_publish_failed",
                event_type=event_name,
                topic=self.topic,
                error=str(e),
            )
            raise
