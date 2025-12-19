# Encrypts customer DB passwords (Crucial!)# security.py
from cryptography.fernet import Fernet
import os

# IN PRODUCTION: Keep this key safe in an Environment Variable!
# For now, we generate one. If you restart the server, you lose access to old keys 
# unless you save this key string specifically.
key = Fernet.generate_key() 
cipher_suite = Fernet(key)

def encrypt_password(password: str) -> str:
    """Encrypts a plain text password."""
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password: str) -> str:
    """Decrypts back to plain text for connecting."""
    return cipher_suite.decrypt(encrypted_password.encode()).decode()