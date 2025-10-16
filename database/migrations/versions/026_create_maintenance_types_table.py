# -*- coding: utf-8 -*-
"""
Migration: Create maintenance_types table
Tabela para armazenar tipos de manutenção
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '026'
down_revision = '025'
branch_labels = None
depends_on = None


def upgrade():
    """Cria a tabela maintenance_types"""
    op.create_table(
        'maintenance_types',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(100), nullable=False, unique=True, comment='Nome do tipo de manutenção'),
        sa.Column('description', sa.Text, nullable=True, comment='Descrição detalhada'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('NOW()'), comment='Data de criação')
    )

    # Criar índice
    op.create_index('idx_maintenance_types_name', 'maintenance_types', ['name'])


def downgrade():
    """Remove a tabela maintenance_types"""
    op.drop_index('idx_maintenance_types_name', table_name='maintenance_types')
    op.drop_table('maintenance_types')
