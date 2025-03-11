from fastapi import FastAPI, HTTPException, Request
import docker
import requests
import os
from api.blockchain import Blockchain
from api.security import encrypt_message
from fastapi.templating import Jinja2Templates

app = FastAPI(debug=True)
templates = Jinja2Templates(directory="api/templates")

# Inicializar Docker y Blockchain
client = docker.from_env()
blockchain = Blockchain()

def propagate_block(block):
    # Lista de nodos en la red interna (pueden usarse los nombres de servicio definidos en docker-compose)
    nodes = ["http://api1:8000", "http://api2:8000", "http://api3:8000"]
    # Si se establece la variable de entorno CONTAINER_NAME, se omite la notificación a sí mismo
    my_name = os.getenv("CONTAINER_NAME", "")
    for node in nodes:
        if my_name and node.startswith(f"http://{my_name}"):
            continue
        try:
            requests.post(f"{node}/receive_block", json=block)
        except Exception as e:
            print(f"Error propagando a {node}: {e}")

@app.get("/")
def home(request: Request):
    try:
        containers = client.containers.list()
        return templates.TemplateResponse("index.html", {"request": request, "containers": containers})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cargando la interfaz: {str(e)}")

@app.get("/containers")
def list_containers():
    try:
        containers = client.containers.list()
        return [{"id": c.id, "name": c.name, "status": c.status} for c in containers]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo contenedores: {str(e)}")

@app.post("/create_image/{container_id}")
def create_container_image(container_id: str, image_name: str):
    try:
        container = client.containers.get(container_id)
        image = container.commit(repository=image_name)
        
        # Registrar la transacción en la blockchain
        transaction_data = f"Imagen creada: {image_name}"
        new_block = blockchain.add_block(transaction_data)
        propagate_block(new_block)
        
        return {"message": "Imagen creada y registrada en Blockchain", "image_id": image.id}
    
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail="Contenedor no encontrado")
    except docker.errors.APIError as e:
        raise HTTPException(status_code=500, detail=f"Error con Docker API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@app.post("/transaction")
def create_transaction(data: dict):
    try:
        encrypted_data = encrypt_message(str(data))
        new_block = blockchain.add_block(encrypted_data)
        propagate_block(new_block)
        return {"message": "Transacción agregada a la blockchain", "hash": encrypted_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la transacción: {str(e)}")

@app.post("/secure_transaction")
def secure_transaction(data: dict):
    try:
        encrypted_data = encrypt_message(str(data))
        # Verificar si la transacción ya está registrada
        for block in blockchain.chain:
            if block.get("data") == encrypted_data:
                return {"message": "Transacción ya registrada", "hash": encrypted_data}
        new_block = blockchain.add_block(encrypted_data)
        propagate_block(new_block)
        return {"message": "Nueva transacción agregada", "hash": encrypted_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la transacción segura: {str(e)}")

@app.get("/blockchain")
def get_blockchain():
    return {"chain": blockchain.chain}

@app.get("/validate_blockchain")
def validate_blockchain():
    if blockchain.is_chain_valid():
        return {"message": "Blockchain es válida"}
    else:
        return {"message": "¡Blockchain ha sido alterada!"}

@app.post("/receive_block")
def receive_block(block: dict):
    try:
        last_block = blockchain.get_previous_block()
        # Verificar que el bloque recibido sea el siguiente en la cadena
        if block["index"] == last_block["index"] + 1 and block["previous_hash"] == blockchain.hash(last_block):
            blockchain.chain.append(block)
            return {"message": "Bloque recibido y agregado"}
        else:
            return {"message": "Bloque no agregado; la cadena puede estar desincronizada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al recibir el bloque: {str(e)}")
