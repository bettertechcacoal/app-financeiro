"""create client_meta table

Revision ID: 018
Revises: 017
Create Date: 2025-10-12

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '018'
down_revision: Union[str, None] = '017'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria tabela client_meta para armazenar metadados dos clientes"""
    op.create_table(
        'client_meta',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('meta_key', sa.String(length=255), nullable=False),
        sa.Column('meta_value', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar índices para otimizar buscas
    op.create_index('idx_client_meta_client_id', 'client_meta', ['client_id'])
    op.create_index('idx_client_meta_meta_key', 'client_meta', ['meta_key'])
    op.create_index('idx_client_meta_client_key', 'client_meta', ['client_id', 'meta_key'], unique=True)


def downgrade() -> None:
    """Remove tabela client_meta"""
    op.drop_index('idx_client_meta_client_key', table_name='client_meta')
    op.drop_index('idx_client_meta_meta_key', table_name='client_meta')
    op.drop_index('idx_client_meta_client_id', table_name='client_meta')
    op.drop_table('client_meta')
