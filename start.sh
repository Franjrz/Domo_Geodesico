#!/bin/bash
set -e

# Start the FastAPI backend
cd /app/backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &

# Wait for the backend to start
sleep 2

# Start Nginx in the foreground
echo "Starting Nginx..."
nginx -g "daemon off;"
