FROM ubuntu:20.04

# Actualiza e instala dependencias, incluyendo Python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    curl \
    vim \
    net-tools

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos e instala las dependencias
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Comando a ejecutar cuando se inicie el contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]