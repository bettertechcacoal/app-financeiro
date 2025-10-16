# -*- coding: utf-8 -*-
"""
Migration: Create vehicles table
Tabela para armazenar dados básicos dos veículos da frota
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


# revision identifiers
revision = '025'
down_revision = '024'
branch_labels = None
depends_on = None


def upgrade():
    """Cria a tabela vehicles"""
    op.create_table(
        'vehicles',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('plate', sa.String(10), nullable=False, unique=True, comment='Placa do veículo'),
        sa.Column('model', sa.String(100), nullable=False, comment='Modelo do veículo'),
        sa.Column('brand', sa.String(50), nullable=False, comment='Marca do veículo'),
        sa.Column('year', sa.Integer, nullable=False, comment='Ano de fabricação'),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True, comment='Veículo ativo'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('NOW()'), comment='Data de criação'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('NOW()'), onupdate=sa.text('NOW()'), comment='Data de atualização')
    )

    # Criar índices
    op.create_index('idx_vehicles_plate', 'vehicles', ['plate'])
    op.create_index('idx_vehicles_is_active', 'vehicles', ['is_active'])


def downgrade():
    """Remove a tabela vehicles"""
    op.drop_index('idx_vehicles_is_active', table_name='vehicles')
    op.drop_index('idx_vehicles_plate', table_name='vehicles')
    op.drop_table('vehicles')
