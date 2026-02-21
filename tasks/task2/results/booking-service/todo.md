# grpc python async booking service

we need to move out the booking service from `/Users/yalobur/projects/courses/yandex/mswa/msa-sprint2/hotelio-monolith`
to a separate python async grpc service

- look at
  `/Users/yalobur/projects/courses/yandex/mswa/msa-sprint2/hotelio-monolith/src/main/java/com/hotelio/monolith/controller/BookingController.java`,
  we need to move the controller to our python service using grpc
- the logic of the controller description is in the `BookingService` class and it uses another services, in our python
  service we need to make rest calls to these services:
    - examples of a rest call are here: `/Users/yalobur/projects/courses/yandex/mswa/msa-sprint2/test/regress.sh`
- protobuf definition is here: `/Users/yalobur/projects/courses/yandex/mswa/msa-sprint2/tasks/task2/booking.proto`

# python booking service expected structure:

```text
booking-service/
├── pyproject.toml                  # зависимости/настройки (или requirements.txt)
├── README.md
├── booking.proto
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── alembic.ini
├── migrations/                     # Alembic 
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 2026_02_14_init.py
├── scripts/
│   └── generate_grpc.sh            # protoc генерация
├── app/
│   ├── __init__.py
│   ├── main.py                     # composition root: wiring + grpc server start
│   ├── settings.py                 # Pydantic BaseSettings / env config
│   ├── common/
│   │   ├── logging.py              # structlog/logging setup
│   │   ├── tracing.py              # request-id / context (опционально)
│   │   ├── errors.py               # доменные исключения + маппинг
│   │   └── time.py                 # helpers (utcnow, etc.)
│   │
│   ├── domain/
│   │   ├── entities/
│   │   │   └── booking.py
│   │   ├── services/
│   │   │   └── pricing_service.py
│   │   └── ports/                  # интерфейсы (порты)
│   │       ├── booking_repository.py
│   │       ├── user_client.py
│   │       └── hotel_client.py
│   │
│   ├── application/
│   │   ├── usecases/
│   │   │   └── booking_usecases.py # create/list booking (оркестрация)
│   │   └── dto/
│   │       └── booking_dto.py       # DTO (опционально, удобно для валидации)
│   │
│   ├── infrastructure/
│   │   ├── db/
│   │   │   ├── engine.py            # create_async_engine
│   │   │   ├── session.py           # async_sessionmaker
│   │   │   └── uow.py               # Unit of Work (опционально, но полезно)
│   │   ├── models/
│   │   │   └── booking_sa.py         # SQLAlchemy модели (таблицы)
│   │   ├── repositories/
│   │   │   └── booking_repo_sa.py    # реализация BookingRepository
│   │   ├── clients/
│   │      └── http/
│   │          ├── base.py           # httpx client, timeouts, retries, headers
│   │          ├── user_client_http.py
│   │          └── hotel_client_http.py
│   │   
│   │       
│   │       
│   │
│   └── transport/
│       └── grpc/
│           ├── interceptors.py       # request-id/logging/error mapping
│           ├── handlers/
│           │   └── booking_handler.py
│           └── generated/
│               ├── booking_pb2.py
│               └── booking_pb2_grpc.py
└── tests/ # optional
    ├── unit/
    │   └── test_booking_usecases.py
    └── integration/
        └── test_grpc_endpoints.py
```

# suggested python packages to use:

package manager is uv

```text
# gRPC
grpcio>=1.60
grpcio-tools>=1.60
protobuf>=4.25

# Database
SQLAlchemy>=2.0
asyncpg
alembic>=1.13

# HTTP clients
httpx

# Config & validation
pydantic>=2.6 (with pydantic-settings)


# Logging
structlog>=24.1


# Retry (optional but recommended)
tenacity>=8.2
```