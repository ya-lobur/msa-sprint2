# Booking Service

gRPC async booking service for Hotelio - microservice extracted from monolith.

## Architecture

This service follows a clean architecture with the following layers:

- **Domain**: Core business entities, ports (interfaces), and domain services
- **Application**: Use cases that orchestrate business logic
- **Infrastructure**: Database repositories, HTTP clients, and external service adapters
- **Transport**: gRPC handlers and interceptors

## Features

- Async Python with gRPC
- PostgreSQL with SQLAlchemy 2.0 async
- Clean Architecture / Hexagonal Architecture
- HTTP clients for external services (User, Hotel, Review, Promo)
- Structured logging with structlog
- Database migrations with Alembic
- Docker and Docker Compose support

## Prerequisites

- Python 3.12+
- uv package manager
- PostgreSQL 15+
- Docker and Docker Compose (for containerized deployment)

## Setup

### Local Development

1. Install dependencies:

```bash
uv sync
```

2. Generate gRPC code from proto file:

```bash
chmod +x scripts/generate_grpc.sh
./scripts/generate_grpc.sh
```

3. Set up environment variables (create `.env` file):

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/booking
GRPC_HOST=0.0.0.0
GRPC_PORT=50051
USER_SERVICE_URL=http://localhost:8080
HOTEL_SERVICE_URL=http://localhost:8080
REVIEW_SERVICE_URL=http://localhost:8080
PROMO_SERVICE_URL=http://localhost:8080
LOG_LEVEL=INFO
```

4. Run database migrations:

```bash
uv run alembic upgrade head
```

5. Start the service:

```bash
uv run python -m app.main
```

### Docker Deployment

1. Build and run with Docker Compose:

```bash
cd docker
docker-compose up --build
```

The service will be available on `localhost:50051`.

## gRPC API

### CreateBooking

Creates a new booking with validation.

**Request:**

```protobuf
message BookingRequest {
    string user_id = 1;
    string hotel_id = 2;
    string promo_code = 3; // optional
}
```

**Response:**

```protobuf
message BookingResponse {
    string id = 1;
    string user_id = 2;
    string hotel_id = 3;
    string promo_code = 4;
    double discount_percent = 5;
    double price = 6;
    string created_at = 7; // ISO-8601
}
```

### ListBookings

List bookings, optionally filtered by user ID.

**Request:**

```protobuf
message BookingListRequest {
    string user_id = 1; // optional, empty for all bookings
}
```

**Response:**

```protobuf
message BookingListResponse {
    repeated BookingResponse bookings = 1;
}
```

## Business Logic

The service implements the following business rules from the original monolith:

### User Validation

- User must be active
- User must not be blacklisted

### Hotel Validation

- Hotel must be operational
- Hotel must be trusted (based on reviews)
- Hotel must not be fully booked

### Pricing

- VIP users: base price 80.0
- Standard users: base price 100.0
- Promo codes apply additional discounts

### External Service Calls

The service makes REST calls to:

- **User Service**: `/api/users/{id}/active`, `/api/users/{id}/blacklisted`, `/api/users/{id}/status`
- **Hotel Service**: `/api/hotels/{id}/operational`, `/api/hotels/{id}/fully-booked`
- **Review Service**: `/api/reviews/hotel/{id}/trusted`
- **Promo Service**: `POST /api/promos/validate?code={code}&userId={userId}`

## Testing with grpcurl

```bash
# Create booking
grpcurl -plaintext -proto booking.proto -d '{"user_id": "test-user-2", "hotel_id": "test-hotel-1", "promo_code": "TESTCODE1"}' \
  localhost:50051 booking.BookingService/CreateBooking

# List all bookings
grpcurl -plaintext -proto booking.proto -d '{}' \
  localhost:50051 booking.BookingService/ListBookings

# List bookings by user
grpcurl -plaintext -proto booking.proto -d '{"user_id": "test-user-2"}' \
  localhost:50051 booking.BookingService/ListBookings
```

## Project Structure

```
booking-service/
├── pyproject.toml
├── README.md
├── booking.proto
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── alembic.ini
├── migrations/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 2026_02_15_0000_init.py
├── scripts/
│   └── generate_grpc.sh
└── app/
├── main.py
├── settings.py
├── common/
│   ├── logging.py
│   ├── errors.py
│   └── time.py
├── domain/
│   ├── entities/
│   │   └── booking.py
│   ├── services/
│   │   └── pricing_service.py
│   └── ports/
│       ├── booking_repository.py
│       ├── user_client.py
│       ├── hotel_client.py
│       └── promo_client.py
├── manager/
│   └── usecases/
│       └── booking_usecases.py
├── infrastructure/
│   ├── db/
│   │   ├── engine.py
│   │   └── session.py
│   ├── models/
│   │   └── booking_sa.py
│   ├── repositories/
│   │   └── booking_repo_sa.py
│   └── clients/
│       └── http/
│           ├── base.py
│           ├── user_client_http.py
│           ├── hotel_client_http.py
│           └── promo_client_http.py
└── transport/
└── grpc/
├── interceptors.py
├── handlers/
│   └── booking_handler.py
└── generated/
├── booking_pb2.py
└── booking_pb2_grpc.py
```