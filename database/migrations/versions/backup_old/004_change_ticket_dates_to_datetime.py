"""change ticket dates to datetime

Revision ID: 004
Revises: 003
Create Date: 2025-10-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '004'
down_revision: Union[str, None] = '003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Altera campos created_date e closed_in de Date para DateTime"""
    # Alterar tipo das colunas de DATE para TIMESTAMP
    op.execute("ALTER TABLE tickets ALTER COLUMN created_date TYPE TIMESTAMP USING created_date::timestamp")
    op.execute("ALTER TABLE tickets ALTER COLUMN closed_in TYPE TIMESTAMP USING closed_in::timestamp")


def downgrade() -> None:
    """Reverte campos created_date e closed_in de DateTime para Date"""
    # Reverter tipo das colunas de TIMESTAMP para DATE
    op.execute("ALTER TABLE tickets ALTER COLUMN created_date TYPE DATE USING created_date::date")
    op.execute("ALTER TABLE tickets ALTER COLUMN closed_in TYPE DATE USING closed_in::date")
