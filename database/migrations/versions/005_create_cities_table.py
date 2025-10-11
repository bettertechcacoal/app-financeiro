"""create cities table

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
    """Cria tabela cities"""
    op.create_table(
        'cities',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('ibge_code', sa.String(length=7), nullable=False),
        sa.Column('state_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['state_id'], ['states.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar índice
    op.create_index('ix_cities_ibge_code', 'cities', ['ibge_code'], unique=True)


def downgrade() -> None:
    """Remove tabela cities"""
    op.drop_index('ix_cities_ibge_code', table_name='cities')
    op.drop_table('cities')
