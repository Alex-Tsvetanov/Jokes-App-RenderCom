#!/bin/bash

# Generate Python gRPC code from proto file
python -m grpc_tools.protoc \
    -I./proto \
    --python_out=./proto \
    --grpc_python_out=./proto \
    ./proto/jokes.proto

echo "✅ Python gRPC code generated"

# Generate JavaScript code for gRPC-Web (for frontend)
# Note: This requires protoc and grpc-web plugin to be installed
# For simplicity, we'll document this separately for the frontend
