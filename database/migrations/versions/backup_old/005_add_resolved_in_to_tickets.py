"""add resolved_in to tickets

Revision ID: 005
Revises: 004
Create Date: 2025-10-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '005'
down_revision: Union[str, None] = '004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Adiciona campo resolved_in à tabela tickets"""
    # Adicionar coluna resolved_in (data de resolução do chat pelo agente)
    op.add_column('tickets', sa.Column('resolved_in', sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Remove campo resolved_in da tabela tickets"""
    # Remover coluna
    op.drop_column('tickets', 'resolved_in')
