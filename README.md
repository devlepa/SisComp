# Sistema de Contenedores y Blockchain con FastAPI y Docker

Este proyecto implementa una **API REST** utilizando **FastAPI** para gestionar contenedores Docker y registrar sus acciones en una **blockchain**. La comunicación entre contenedores se asegura mediante encriptación **SHA-256**, y la persistencia de la blockchain se logra mediante un volumen compartido en Docker.

---

## Tabla de Contenidos

- [Características](#caracter%C3%ADsticas)
- [Arquitectura del Proyecto](#arquitectura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación y Configuración](#instalaci%C3%B3n-y-configuraci%C3%B3n)
- [Uso de la Aplicación](#uso-de-la-aplicaci%C3%B3n)
  - [Interfaz Web](#interfaz-web)
  - [Uso de Endpoints con cURL](#uso-de-endpoints-con-curl)
- [Persistencia y Volumen Compartido](#persistencia-y-volumen-compartido)
- [Consideraciones Adicionales](#consideraciones-adicionales)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

---

## Características

- **Gestión de Contenedores:**  
  Visualiza y administra contenedores Docker a través de la API.

- **Creación de Imágenes:**  
  Crea imágenes de contenedores y registra la acción en la blockchain.

- **Blockchain Distribuida:**  
  Cada transacción se agrega a una cadena de bloques, garantizando la integridad y trazabilidad de los cambios.

- **Encriptación SHA-256:**  
  Asegura la información intercambiada entre contenedores.

- **Persistencia de Datos:**  
  La blockchain se guarda en un archivo JSON compartido mediante un volumen Docker, de modo que todos los contenedores accedan a la misma información, incluso después de reinicios.

- **Sincronización entre Contenedores:**  
  Los contenedores se comunican y actualizan la blockchain entre sí a través de endpoints REST.

---

## Arquitectura del Proyecto

La estructura del proyecto es la siguiente:

```
project/
├── api/
│   ├── main.py          # API REST con FastAPI y lógica de propagación de bloques
│   ├── blockchain.py    # Implementación de la blockchain con persistencia en JSON
│   ├── security.py      # Funciones de encriptación SHA-256
│   └── templates/
│       └── index.html   # Interfaz web para interactuar con la API
├── Dockerfile           # Construcción de la imagen basada en Ubuntu 20.04
├── docker-compose.yml   # Orquestación de múltiples contenedores
└── requirements.txt     # Dependencias del proyecto
```

---

## Requisitos

- **Docker** y **Docker Compose**  
- **Python 3** (incluido en la imagen base de Ubuntu)

---

## Instalación y Configuración

1. **Clona el repositorio:**

   ```bash
   git clone https://tu-repositorio.git
   cd project
   ```

2. **Construye y levanta los contenedores:**

   - Detén contenedores anteriores (si existen):
     
     ```bash
     docker-compose down --volumes
     ```
     
   - Construye las imágenes sin caché:
     
     ```bash
     docker-compose build --no-cache
     ```
     
   - Levanta los contenedores en modo background:
     
     ```bash
     docker-compose up -d
     ```

3. **Verifica que los contenedores estén en ejecución:**

   ```bash
   docker ps
   ```

---

## Uso de la Aplicación

### Interfaz Web

Abre tu navegador y visita las siguientes direcciones para acceder a la interfaz web:

- [http://0.0.0.0:8001](http://0.0.0.0:8001)
- [http://0.0.0.0:8002](http://0.0.0.0:8002)
- [http://0.0.0.0:8003](http://0.0.0.0:8003)

La interfaz web ofrece las siguientes funcionalidades mediante botones y formularios:

- **Listar Contenedores:** Muestra la lista de contenedores disponibles.
- **Crear Imagen de Contenedor:** Permite generar una imagen de un contenedor y registra la acción en la blockchain.
- **Ver y Validar la Blockchain:** Permite visualizar la cadena de bloques y comprobar su integridad.
- **Agregar Transacción:** Agrega una nueva transacción a la blockchain.
- **Transacción Segura:** Agrega una transacción segura, verificando que no se duplique la información.

### Uso de Endpoints con cURL

Puedes probar la API utilizando cURL. Aquí algunos ejemplos:

- **Listar contenedores:**

  ```bash
  curl -X GET http://localhost:8001/containers
  ```

- **Crear imagen de contenedor y registrar en la blockchain:**

  ```bash
  curl -X POST "http://localhost:8001/create_image/<container_id>?image_name=nombre_imagen"
  ```

- **Ver la blockchain:**

  ```bash
  curl -X GET http://localhost:8001/blockchain
  ```

- **Agregar una transacción:**

  ```bash
  curl -X POST http://localhost:8001/transaction -H 'Content-Type: application/json' -d '{"data": "Datos de transacción"}'
  ```

- **Transacción segura:**

  ```bash
  curl -X POST http://localhost:8001/secure_transaction -H 'Content-Type: application/json' -d '{"data": "Datos seguros"}'
  ```

- **Validar la blockchain:**

  ```bash
  curl -X GET http://localhost:8001/validate_blockchain
  ```

---

## Persistencia y Volumen Compartido

La blockchain se guarda en el archivo `/app/data/blockchain.json`. Todos los contenedores montan un volumen compartido denominado `blockchain_data` en la ruta `/app/data`, lo que garantiza que:

- **Sincronización:** Todos los cambios realizados en la blockchain desde cualquier contenedor se guardan en el mismo archivo compartido.
- **Persistencia:** Si un contenedor se reinicia, cargará la blockchain actualizada desde el volumen compartido.

El volumen se define en el archivo **docker-compose.yml**:

```yaml
volumes:
  blockchain_data:
```

---

## Consideraciones Adicionales

- **Sincronización en Tiempo Real:**  
  La propagación de bloques se realiza mediante endpoints que actualizan la blockchain entre contenedores activos. Con la persistencia en un volumen compartido, se mantiene la información cuando se reinician los contenedores.

- **Concurrencia:**  
  En entornos de alta concurrencia, puede ser necesario implementar mecanismos de bloqueo o migrar la persistencia a una base de datos para evitar conflictos en el acceso concurrente al archivo.

- **Personalización:**  
  Puedes modificar la lógica de la blockchain, la dificultad del proof-of-work y los endpoints según tus necesidades.

---

## Contribuir

Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tus cambios:

   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

3. Realiza tus modificaciones y haz commit:

   ```bash
   git commit -m "Agrega nueva funcionalidad"
   ```
