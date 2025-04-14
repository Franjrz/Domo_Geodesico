# Etapa de construcción para React
FROM node:18-alpine AS frontend-build

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Etapa de configuración del backend y servidor
FROM python:3.11-slim

# Instalar Nginx
RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configurar backend
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .

# Copiar los archivos del frontend compilado
COPY --from=frontend-build /app/frontend/build /var/www/html

# Configurar Nginx
COPY nginx.conf /etc/nginx/sites-available/default

# Script de inicio
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80

# Iniciar Nginx y el backend de FastAPI
CMD ["/start.sh"]