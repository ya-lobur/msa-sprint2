#!/bin/bash
set -e

echo "Generating gRPC code from booking.proto..."

# Create output directory
mkdir -p app/transport/grpc/generated

# Generate Python gRPC code
uv run -m grpc_tools.protoc \
    -I. \
    --python_out=app/transport/grpc/generated \
    --grpc_python_out=app/transport/grpc/generated \
    --pyi_out=app/transport/grpc/generated \
    booking.proto

# Fix imports in generated files
sed -i.bak 's/^import booking_pb2/from . import booking_pb2/' app/transport/grpc/generated/booking_pb2_grpc.py
rm -f app/transport/grpc/generated/booking_pb2_grpc.py.bak

# Create __init__.py
touch app/transport/grpc/generated/__init__.py

echo "✅ gRPC code generated successfully!"
