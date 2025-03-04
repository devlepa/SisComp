import hashlib
import time

class Blockchain:
    def __init__(self):
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

            if not str(current_block["proof"]).startswith("0000"):
                return False

        return True
