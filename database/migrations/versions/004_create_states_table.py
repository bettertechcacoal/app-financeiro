"""create states table

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
    """Cria tabela states"""
    op.create_table(
        'states',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('uf', sa.String(length=2), nullable=False),
        sa.Column('ibge_code', sa.String(length=2), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar índices
    op.create_index('ix_states_uf', 'states', ['uf'], unique=True)
    op.create_index('ix_states_ibge_code', 'states', ['ibge_code'], unique=True)


def downgrade() -> None:
    """Remove tabela states"""
    op.drop_index('ix_states_ibge_code', table_name='states')
    op.drop_index('ix_states_uf', table_name='states')
    op.drop_table('states')
