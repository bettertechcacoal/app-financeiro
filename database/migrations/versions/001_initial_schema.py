"""initial schema

Revision ID: 001
Revises:
Create Date: 2025-10-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Criar tabela organizations
    op.create_table(
        'organizations',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('business_name', sa.String(length=255), nullable=False),
        sa.Column('person_type', sa.String(length=20), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar tabela clients
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('document', sa.String(length=50), nullable=False),
        sa.Column('organization_id', sa.String(length=50), nullable=True),
        sa.Column('address', sa.String(length=500), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('state', sa.String(length=2), nullable=True),
        sa.Column('zipcode', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('document')
    )

    # Criar tabela client_organizations (relação muitos-para-muitos)
    op.create_table(
        'client_organizations',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('organization_id', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('client_id', 'organization_id', name='unique_client_organization')
    )

    # Criar tabela sync_logs
    op.create_table(
        'sync_logs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('sync_type', sa.String(length=50), nullable=False),
        sa.Column('total', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('synced', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('updated', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('errors', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('synced_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar tabela tickets
    op.create_table(
        'tickets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('subject', sa.String(length=500), nullable=True),
        sa.Column('status', sa.String(length=100), nullable=True),
        sa.Column('service_full', sa.String(length=500), nullable=True),
        sa.Column('organization_name', sa.String(length=255), nullable=True),
        sa.Column('client_name', sa.String(length=255), nullable=True),
        sa.Column('owner_name', sa.String(length=255), nullable=True),
        sa.Column('created_by_name', sa.String(length=255), nullable=True),
        sa.Column('created_by_email', sa.String(length=255), nullable=True),
        sa.Column('created_date', sa.Date(), nullable=True),
        sa.Column('closed_in', sa.Date(), nullable=True),
        sa.Column('custom_field_module', sa.String(length=255), nullable=True),
        sa.Column('synced_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar índices
    op.create_index('idx_client_organizations_client_id', 'client_organizations', ['client_id'])
    op.create_index('idx_client_organizations_organization_id', 'client_organizations', ['organization_id'])
    op.create_index('idx_clients_organization_id', 'clients', ['organization_id'])
    op.create_index('idx_clients_document', 'clients', ['document'])


def downgrade() -> None:
    # Remover índices (com IF EXISTS para evitar erros)
    op.execute('DROP INDEX IF EXISTS idx_clients_document')
    op.execute('DROP INDEX IF EXISTS idx_clients_organization_id')
    op.execute('DROP INDEX IF EXISTS idx_client_organizations_organization_id')
    op.execute('DROP INDEX IF EXISTS idx_client_organizations_client_id')

    # Remover tabelas (com IF EXISTS para evitar erros)
    op.execute('DROP TABLE IF EXISTS tickets CASCADE')
    op.execute('DROP TABLE IF EXISTS sync_logs CASCADE')
    op.execute('DROP TABLE IF EXISTS client_organizations CASCADE')
    op.execute('DROP TABLE IF EXISTS clients CASCADE')
    op.execute('DROP TABLE IF EXISTS organizations CASCADE')
