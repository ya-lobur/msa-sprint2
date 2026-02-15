FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy proto file and generate gRPC code
COPY booking.proto ./
COPY scripts/generate_grpc.sh scripts/
RUN chmod +x scripts/generate_grpc.sh && \
    uv run python -m grpc_tools.protoc \
    -I. \
    --python_out=app/transport/grpc/generated \
    --grpc_python_out=app/transport/grpc/generated \
    --pyi_out=app/transport/grpc/generated \
    booking.proto && \
    mkdir -p app/transport/grpc/generated && \
    touch app/transport/grpc/generated/__init__.py && \
    sed -i 's/^import booking_pb2/from . import booking_pb2/' app/transport/grpc/generated/booking_pb2_grpc.py || true

# Copy application code
COPY app/ app/
COPY alembic.ini ./
COPY migrations/ migrations/

# Expose gRPC port
EXPOSE 50051

# Run migrations and start server
CMD ["sh", "-c", "uv run alembic upgrade head && uv run python -m app.main"]
