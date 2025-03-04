from fastapi import FastAPI, HTTPException, Request
import docker
from blockchain import Blockchain
from security import encrypt_message
from fastapi.templating import Jinja2Templates

app = FastAPI(debug=True)
templates = Jinja2Templates(directory="api/templates")

# Inicializar Docker y Blockchain
client = docker.from_env()
blockchain = Blockchain()

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
        
        # ✅ Registrar la transacción en la blockchain
        transaction_data = f"Imagen creada: {image_name}"
        blockchain.add_block(transaction_data)
        
        return {"message": "Imagen creada y registrada en Blockchain", "image_id": image.id}
    
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail="Contenedor no encontrado")
    except docker.errors.APIError as e:
        raise HTTPException(status_code=500, detail=f"Error con Docker API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# ✅ **Ver la blockchain completa**
@app.get("/blockchain")
def get_blockchain():
    return {"chain": blockchain.chain}

# ✅ **Agregar una transacción a la blockchain**
@app.post("/transaction")
def create_transaction(data: dict):
    try:
        encrypted_data = encrypt_message(str(data))
        blockchain.add_block(encrypted_data)
        return {"message": "Transaction added to blockchain", "hash": encrypted_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la transacción: {str(e)}")

# ✅ **Verificar si una transacción ya está en la blockchain**
@app.post("/secure_transaction")
def secure_transaction(data: dict):
    try:
        encrypted_data = encrypt_message(str(data))

        # Verificar si el hash ya existe en la blockchain
        for block in blockchain.chain:
            if block.get("data") == encrypted_data:
                return {"message": "Transacción ya registrada", "hash": encrypted_data}

        # Si no existe, se agrega
        blockchain.add_block(encrypted_data)
        return {"message": "Nueva transacción agregada", "hash": encrypted_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la transacción segura: {str(e)}")

# ✅ **Verificar la integridad de la blockchain**
@app.get("/validate_blockchain")
def validate_blockchain():
    if blockchain.is_chain_valid():
        return {"message": "Blockchain es válida"}
    else:
        return {"message": "¡Blockchain ha sido alterada!"}
