<<<<<<< HEAD
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js and npm for frontend
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install dependencies
COPY backend/requirements.txt /app/backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend/ /app/backend/

# Copy frontend code
COPY frontend/ /app/frontend/

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy startup script
COPY start.sh /app/
RUN chmod +x /app/start.sh

# Expose ports
EXPOSE 80

# Set the startup command
CMD ["/app/start.sh"]
=======
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
>>>>>>> 40143b4a9a8e37ee2dbf53e26c63feefa92b4e01
