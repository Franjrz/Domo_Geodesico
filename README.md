# Domo Geodésico

Este proyecto contiene una aplicación full-stack con un backend FastAPI y un frontend simple, todo ejecutándose en un único contenedor Docker.

## Estructura del Proyecto

- `backend/`: Contiene el código del backend FastAPI
  - `main.py`: Aplicación principal FastAPI con endpoints de ejemplo
  - `requirements.txt`: Dependencias de Python
- `frontend/`: Contiene el código del frontend
  - `index.html`: Página HTML simple para probar la conexión con la API
- `Dockerfile`: Configuración para construir la imagen Docker
- `nginx.conf`: Configuración de Nginx para el enrutamiento
- `start.sh`: Script de inicio para el contenedor Docker
- `.gitignore`: Configuración para excluir archivos innecesarios del control de versiones

## Construcción y Ejecución

### Prerrequisitos

- Docker instalado en tu sistema

### Construir la Imagen Docker

```bash
docker build -t domo-geodesico .
```

### Ejecutar el Contenedor Docker

```bash
docker run -p 80:80 domo-geodesico
```

La aplicación estará disponible en http://localhost

## Desarrollo

- La API del backend es accesible en `/api/`
- La documentación de la API está disponible en `/docs`
- El frontend se sirve desde la ruta raíz `/`

## Notas

- Esta es una configuración básica con un endpoint de API de ejemplo
- El backend se ampliará con más funcionalidades según se especifique
