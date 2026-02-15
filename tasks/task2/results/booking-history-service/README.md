# Booking History Service

A Kafka consumer service that listens to `BookingCreated` events and stores booking history in a PostgreSQL database.

## Architecture

This service follows clean architecture principles with the following layers:

- **Domain Layer**: Entities, events, and repository interfaces
- **Infrastructure Layer**: Database models, repositories, Kafka consumer
- **Manager Layer**: Use cases and business logic
- **Common Layer**: Shared utilities (logging, etc.)

## Features

- Consumes `BookingCreated` events from Kafka topic `booking-events`
- Stores booking history in PostgreSQL database
- Async/await architecture using asyncio and aiokafka
- SQLAlchemy 2.0 with async support
- Structured logging with structlog
- Database migrations with Alembic
- Configuration via environment variables

## Requirements

- Python 3.12+
- PostgreSQL
- Kafka

## Installation

### Local Development

Install dependencies using uv:

```bash
uv sync
```

### Docker

Build and run using Docker Compose:

```bash
# Run standalone (includes Kafka, Zookeeper, and PostgreSQL)
cd docker
docker-compose up --build

# Or run as part of the full task2 system
cd ../../..
docker-compose up --build booking-history-service
```

## Configuration

Configure the service using environment variables or `.env` file:

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5434/booking_history

# Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=booking-events
KAFKA_GROUP_ID=booking-history-service

# Logging
LOG_LEVEL=INFO
```

## Database Setup

Run Alembic migrations to create the database schema:

```bash
uv run alembic upgrade head
```

This creates the `booking_history` table with the following columns:

- `id`: Auto-incrementing primary key
- `booking_id`: Booking ID from the event (indexed, unique)
- `user_id`: User ID (indexed)
- `hotel_id`: Hotel ID (indexed)
- `promo_code`: Optional promo code
- `discount_percent`: Discount percentage applied
- `price`: Final price after discount
- `created_at`: Booking creation timestamp

## Running the Service

### Local Development

Start the service:

```bash
python -m app.main
```

Or using uv:

```bash
uv run python -m app.main
```

### Docker

Run with Docker Compose:

```bash
# Standalone mode
cd docker
docker-compose up

# As part of the full system
cd ../../..
docker-compose up booking-history-service
```

The service will:

1. Connect to Kafka and subscribe to the `booking-events` topic
2. Listen for `BookingCreated` events
3. Parse and validate incoming events
4. Store booking history in the database
5. Log all operations with structured logging

## Event Format

The service expects `BookingCreated` events in the following format:

```json
{
  "event_type": "BookingCreated",
  "data": {
    "id": "13",
    "user_id": "test-user-2",
    "hotel_id": "test-hotel-1",
    "price": 90.0,
    "promo_code": "TESTCODE1",
    "discount_percent": 10.0,
    "created_at": "2026-02-15T14:37:34.859067+00:00"
  }
}
```

## Project Structure

```
booking-history-service/
├── app/
│   ├── domain/
│   │   ├── entities/
│   │   │   └── booking_history.py          # BookingHistory domain entity
│   │   ├── events/
│   │   │   └── booking_created.py          # BookingCreated event (same as booking-service)
│   │   └── ports/
│   │       └── booking_history_repository.py  # Repository interface
│   ├── infrastructure/
│   │   ├── db/
│   │   │   ├── engine.py                   # Database engine config
│   │   │   └── session.py                  # Session factory
│   │   ├── models/
│   │   │   └── booking_history_sa.py       # SQLAlchemy model
│   │   ├── repositories/
│   │   │   └── booking_history_repo_sa.py  # Repository implementation
│   │   └── messaging/
│   │       └── kafka_consumer.py           # Kafka consumer wrapper
│   ├── manager/
│   │   └── usecases/
│   │       └── booking_history_usecases.py # Use cases
│   ├── common/
│   │   └── logging.py                      # Logging setup
│   ├── settings.py                         # Application settings
│   └── main.py                             # Main entry point
├── alembic/
│   ├── versions/
│   │   └── 001_initial_migration.py        # Database migration
│   ├── env.py                              # Alembic environment
│   └── script.py.mako                      # Migration template
├── alembic.ini                             # Alembic config
└── pyproject.toml                          # Updated with description
```

## Development

### Creating New Migrations

To create a new migration after modifying models:

```bash
alembic revision --autogenerate -m "description"
```

### Viewing Migration History

```bash
alembic history
```

### Rolling Back Migrations

```bash
alembic downgrade -1
```

## Logging

The service uses structured logging with the following information:

- Log level
- Module name and line number
- ISO timestamp
- Event context (booking_id, user_id, etc.)

Example log output:

```
2026-02-15T14:37:35.123456 [info     ] processing_booking_created_event booking_id=13 hotel_id=test-hotel-1 user_id=test-user-2 [app.manager.usecases.booking_history_usecases:24]
2026-02-15T14:37:35.234567 [info     ] booking_history_saved booking_id=13 hotel_id=test-hotel-1 id=1 user_id=test-user-2 [app.infrastructure.repositories.booking_history_repo_sa:40]
```

## Error Handling

- Failed event parsing logs an error and raises an exception
- Database errors trigger a rollback and log the error
- Unknown event types are logged and ignored
- The service continues processing other messages after errors

## Graceful Shutdown

The service handles `SIGINT` and `SIGTERM` signals for graceful shutdown:

1. Stop consuming new messages
2. Wait for current message processing to complete
3. Close Kafka consumer
4. Dispose database connections
5. Exit cleanly
