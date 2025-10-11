"""add category field to tickets

Revision ID: 003
Revises: 002
Create Date: 2025-10-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Adiciona campo category à tabela tickets"""
    # Adicionar coluna category
    op.add_column('tickets', sa.Column('category', sa.String(length=100), nullable=True))


def downgrade() -> None:
    """Remove campo category da tabela tickets"""
    # Remover coluna
    op.drop_column('tickets', 'category')
