from sqlalchemy.types import TypeDecorator, Text
from app.security import encrypt_value, decrypt_value

class EncryptedString(TypeDecorator):
    # SQLAlchemy Custom Column that will automatically encrypt values.
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return encrypt_value(value)
    
    def process_result_value(self, value, dialect):
        return value

def decrypt_encrypted_field(value):
    # Decrypt a value that was encrypted using EncryptedString column type
    return decrypt_value(value)