#!/bin/bash

echo "🚀 Setting up Jokes Streamer Application"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

echo "✅ Node.js found: $(node --version)"

# Setup Backend
echo ""
echo "📦 Setting up backend..."
cd backend

# Install Python dependencies
echo "  Installing Python dependencies..."
pip install -r requirements.txt

# Generate gRPC code
echo "  Generating gRPC code from proto files..."
python -m grpc_tools.protoc \
    -I./proto \
    --python_out=./proto \
    --grpc_python_out=./proto \
    ./proto/jokes.proto

echo "✅ Backend setup complete!"

# Setup Frontend
cd ../frontend
echo ""
echo "📦 Setting up frontend..."
echo "  Installing Node dependencies..."
npm install

echo "✅ Frontend setup complete!"

cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To run the application locally:"
echo ""
echo "1. Set up a PostgreSQL database and set DATABASE_URL:"
echo "   export DATABASE_URL='postgresql://user:password@localhost/jokes_db'"
echo ""
echo "2. Start the backend:"
echo "   cd backend && python server.py"
echo ""
echo "3. In a new terminal, start the frontend:"
echo "   cd frontend && REACT_APP_BACKEND_URL=http://localhost:8000 npm start"
echo ""
