#!/bin/bash

# Quick start script for local development
# This assumes PostgreSQL is already running locally

echo "🚀 Starting Jokes Streamer in development mode..."

# Set default environment variables
export DATABASE_URL="${DATABASE_URL:-postgresql://postgres:postgres@localhost/jokes_db}"
export REACT_APP_BACKEND_URL="http://localhost:8000"

echo "📊 Using database: $DATABASE_URL"
echo ""

# Start backend in background
echo "🔧 Starting backend server..."
cd backend
python server.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 3

# Start frontend
echo "🎨 Starting frontend development server..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Application started!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔌 Backend HTTP API: http://localhost:8000"
echo "🔌 Backend gRPC: localhost:50051"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
