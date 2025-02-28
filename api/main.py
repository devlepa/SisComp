from fastapi import FastAPI, HTTPException
import docker
import hashlib
import requests
from api.blockchain import Blockchain
from api.security import encrypt_message
 
 
app = FastAPI()
 
 
# Inicializar Docker y Blockchain
client = docker.from_env()
blockchain = Blockchain()
 
 
# Endpoint para listar los contenedores activos
@app.get("/containers")
def list_containers():
    containers = client.containers.list()
    return [{"id": container.id, "name": container.name, "status": container.status} for container in containers]
 
 
# Endpoint para crear una imagen del contenedor
@app.post("/create_image/{container_id}")
def create_container_image(container_id: str, image_name: str):
    try:
        container = client.containers.get(container_id)
        image = container.commit(repository=image_name)
        return {"message": "Imagen creada", "image_id": image.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
 
 
# Endpoint para realizar una transacción en la blockchain
@app.post("/transaction")
def create_transaction(data: dict):
    encrypted_data = encrypt_message(str(data))
    blockchain.add_block(encrypted_data)
    return {"message": "Transaction added to blockchain", "hash": encrypted_data}
 
@app.post("/secure_transaction")
def secure_transaction(data: dict):
    encrypted_data = encrypt_message(str(data))
 
 
    # Verificar si el hash ya existe en la blockchain
    for block in blockchain.chain:
        if block.get("data") == encrypted_data:
            return {"message": "Transacción ya registrada", "hash": encrypted_data}
 
 
    # Si no existe, se agrega
    blockchain.add_block(encrypted_data)
    return {"message": "Nueva transacción agregada", "hash": encrypted_data}