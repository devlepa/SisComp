FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias y utilidades
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    curl \
    vim \
    net-tools && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Crea el directorio para persistencia de datos
RUN mkdir -p /app/data

# Declara el volumen para docker.sock
VOLUME ["/var/run/docker.sock"]

# Copia el archivo de requerimientos e instala las dependencias de Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install jinja2

# Copia el resto del código de la aplicación
COPY . .

# Exponer el puerto en el que correrá FastAPI
EXPOSE 8000

# Inicia la aplicación indicando la ubicación correcta de main.py (dentro de api/)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
