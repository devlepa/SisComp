import hashlib
 
 
def encrypt_message(message: str) -> str:
    return hashlib.sha256(message.encode()).hexdigest()