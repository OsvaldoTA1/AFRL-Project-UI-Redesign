from cryptography.fernet import Fernet # Encrypting and Decrypting before it enters the database.
import cred

COLLECT_IPS = getattr(cred, 'COLLECT_IPS', True)
IP_ENCRYPTION_KEY = getattr(cred, 'IP_ENCRYPTION_KEY', None)

def get_fernet():
    if not IP_ENCRYPTION_KEY:
        return None
    try:
        return Fernet(IP_ENCRYPTION_KEY.encode())
    except ValueError:
        print("Invalid Fernet Key! Encryption will be disabled.")
        return None

def encrypt_value(value: str) -> str | None:
    if not COLLECT_IPS or not value:
        return None
    f = get_fernet()
    if f is None:
        return None
    return f.encrypt(value.encode()).decode()

def decrypt_value(value: str) -> str | None:
    if not COLLECT_IPS or not value:
        return None
    f = get_fernet()
    if f is None:
        return value
    return f.decrypt(value.encode()).decode()