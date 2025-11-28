#!/bin/bash

# Function to kill background processes on exit
trap 'kill $(jobs -p)' EXIT

echo "Starting Agent Factory..."

# Start Backend
echo "Starting Backend (FastAPI)..."
uvicorn server.main:app --reload --port 8000 &
BACKEND_PID=$!

# Start Frontend
echo "Starting Frontend (Vite)..."
cd client
npm run dev &
FRONTEND_PID=$!
cd ..

echo "Agent Factory is running!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
