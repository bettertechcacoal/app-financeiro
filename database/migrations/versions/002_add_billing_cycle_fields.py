"""add billing cycle fields to clients

Revision ID: 002
Revises: 001
Create Date: 2025-10-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Adiciona campos de ciclo de cobrança à tabela clients"""
    # Adicionar coluna billing_cycle_type
    op.add_column('clients', sa.Column('billing_cycle_type', sa.String(length=20), nullable=True))

    # Adicionar coluna fixed_start_day
    op.add_column('clients', sa.Column('fixed_start_day', sa.Integer(), nullable=True))


def downgrade() -> None:
    """Remove campos de ciclo de cobrança da tabela clients"""
    # Remover colunas
    op.drop_column('clients', 'fixed_start_day')
    op.drop_column('clients', 'billing_cycle_type')
