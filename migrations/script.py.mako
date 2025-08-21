"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# import custom types
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    from app.custom_types import EncryptedString, decrypt_encrypted_field
    # Make them available in the global namespace for the migration
    globals()['EncryptedString'] = EncryptedString
    globals()['decrypt_encrypted_field'] = decrypt_encrypted_field
except ImportError as e:
    # Fallback for migrations that don't need custom types
    print(f"Warning: Could not import custom types: {e}")
    class EncryptedString:
        pass
    globals()['EncryptedString'] = EncryptedString

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
    ${downgrades if downgrades else "pass"}
