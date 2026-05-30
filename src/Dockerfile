# Una imagen ligera de Python para simular el dispositivo IoT
FROM python:3.11-slim

# Evitamos que Python genere archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalación de curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# El contenedor ejecuta el parche
CMD ["python", "patch_test.py"]