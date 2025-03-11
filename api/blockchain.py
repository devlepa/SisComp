import hashlib
import time
import json
import os

class Blockchain:
    def __init__(self, file_path="/app/data/blockchain.json"):
        self.file_path = file_path
        self.chain = []
        # Si existe el archivo de la blockchain, lo carga; si no, crea el bloque génesis.
        if os.path.exists(self.file_path):
            self.load_chain()
        else:
            self.create_genesis_block()
            self.save_chain()

    def create_genesis_block(self):
        self.chain = []
        self.create_block(proof=1, previous_hash="0", data="Genesis Block")

    def create_block(self, proof, previous_hash, data):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time.time(),
            "proof": proof,
            "previous_hash": previous_hash,
            "data": data
        }
        self.chain.append(block)
        self.save_chain()
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        while True:
            hash_value = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_value[:4] == "0000":  # Condición de dificultad
                return new_proof
            new_proof += 1

    def add_block(self, data):
        previous_block = self.get_previous_block()
        proof = self.proof_of_work(previous_block["proof"])
        previous_hash = self.hash(previous_block)
        return self.create_block(proof, previous_hash, data)

    def hash(self, block):
        return hashlib.sha256(str(block).encode()).hexdigest()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block["previous_hash"] != self.hash(previous_block):
                return False
            previous_proof = previous_block["proof"]
            current_proof = current_block["proof"]
            hash_operation = hashlib.sha256(str(current_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False
        return True

    def save_chain(self):
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.chain, f, indent=4)
        except Exception as e:
            print("Error guardando la blockchain:", e)

    def load_chain(self):
        try:
            with open(self.file_path, 'r') as f:
                self.chain = json.load(f)
        except Exception as e:
            print("Error cargando la blockchain:", e)
            self.chain = []
