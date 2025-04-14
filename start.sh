#!/bin/bash
<<<<<<< HEAD
set -e

# Start the FastAPI backend
cd /app/backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &

# Wait for the backend to start
sleep 2

# Start Nginx in the foreground
echo "Starting Nginx..."
nginx -g "daemon off;"
=======

# Iniciar el backend en segundo plano
cd /app/backend
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Iniciar Nginx en primer plano
nginx -g "daemon off;"
>>>>>>> 40143b4a9a8e37ee2dbf53e26c63feefa92b4e01
