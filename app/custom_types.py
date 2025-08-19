from sqlalchemy.types import TypeDecorator, Text
from app.security import encrypt_value, decrypt_value

class EncryptedString(TypeDecorator):
    # SQLAlchemy Custom Column that will automatically encrypt values.
    impl = Text

    def process_bind_param(self, value, dialect):
        return encrypt_value(value)
    
    def process_result_value(self, value, dialect):
        return value

def decrypt_field(value):
    return decrypt_value(value)