"""create clients table

Revision ID: 008
Revises: 007
Create Date: 2025-10-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '008'
down_revision: Union[str, None] = '007'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria tabela clients"""
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('document', sa.String(length=50), nullable=False),
        sa.Column('organization_id', sa.String(length=50), nullable=True),
        sa.Column('address', sa.String(length=500), nullable=True),
        sa.Column('city_id', sa.Integer(), nullable=True),
        sa.Column('state', sa.String(length=2), nullable=True),
        sa.Column('zipcode', sa.String(length=20), nullable=True),
        sa.Column('billing_cycle', sa.Integer(), nullable=True),
        sa.Column('billing_day', sa.Integer(), nullable=True),
        sa.Column('billing_cycle_type', sa.String(length=20), nullable=True),
        sa.Column('fixed_start_day', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id']),
        sa.ForeignKeyConstraint(['city_id'], ['cities.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('document')
    )

    # Criar índices
    op.create_index('idx_clients_document', 'clients', ['document'])
    op.create_index('idx_clients_organization_id', 'clients', ['organization_id'])
    op.create_index('idx_clients_city_id', 'clients', ['city_id'])


def downgrade() -> None:
    """Remove tabela clients"""
    op.drop_index('idx_clients_organization_id', table_name='clients')
    op.drop_index('idx_clients_document', table_name='clients')
    op.drop_table('clients')
