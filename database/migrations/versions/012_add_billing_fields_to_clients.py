"""add billing_cycle_type and fixed_start_day to clients

Revision ID: 012
Revises: 011
Create Date: 2025-10-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '012'
down_revision: Union[str, None] = '011'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Adiciona colunas billing_cycle_type e fixed_start_day na tabela clients"""
    op.add_column('clients', sa.Column('billing_cycle_type', sa.String(length=20), nullable=True))
    op.add_column('clients', sa.Column('fixed_start_day', sa.Integer(), nullable=True))


def downgrade() -> None:
    """Remove colunas billing_cycle_type e fixed_start_day da tabela clients"""
    op.drop_column('clients', 'fixed_start_day')
    op.drop_column('clients', 'billing_cycle_type')
