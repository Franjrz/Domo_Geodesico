#!/bin/bash

# Iniciar el backend en segundo plano
cd /app/backend
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Iniciar Nginx en primer plano
nginx -g "daemon off;"
