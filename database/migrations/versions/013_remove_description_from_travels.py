"""remove description from travels

Revision ID: 013
Revises: 012
Create Date: 2025-10-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '013'
down_revision: Union[str, None] = '012'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove coluna description da tabela travels"""
    op.drop_column('travels', 'description')


def downgrade() -> None:
    """Adiciona coluna description de volta na tabela travels"""
    op.add_column('travels', sa.Column('description', sa.Text(), nullable=True))
