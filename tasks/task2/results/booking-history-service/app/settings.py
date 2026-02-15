"""Application settings using Pydantic BaseSettings."""
from functools import cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5434/booking_history",
        description="Database URL",
    )

    # Kafka
    kafka_bootstrap_servers: str = Field(default="localhost:9092", description="Kafka bootstrap servers")
    kafka_topic: str = Field(default="booking-events", description="Kafka topic name")
    kafka_group_id: str = Field(default="booking-history-service", description="Kafka consumer group ID")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")


@cache
def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
