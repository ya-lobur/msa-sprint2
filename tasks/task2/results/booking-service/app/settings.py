"""Application settings using Pydantic BaseSettings."""
from functools import cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5433/booking",
        description="Database URL",
    )

    # gRPC Server
    grpc_host: str = Field(default="0.0.0.0", description="gRPC server host")
    grpc_port: int = Field(default=50051, description="gRPC server port")

    # External Services
    user_service_url: str = Field(default="http://localhost:8080", description="User service URL")
    hotel_service_url: str = Field(default="http://localhost:8080", description="Hotel service URL")
    review_service_url: str = Field(default="http://localhost:8080", description="Review service URL")
    promo_service_url: str = Field(default="http://localhost:8080", description="Promo service URL")

    # Kafka
    kafka_bootstrap_servers: str = Field(default="localhost:9092", description="Kafka bootstrap servers")
    kafka_topic: str = Field(default="booking-events", description="Kafka topic name")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")

@cache
def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
