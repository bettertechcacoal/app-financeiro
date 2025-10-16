# -*- coding: utf-8 -*-
"""
Migration: Create vehicle_meta table
Tabela para armazenar metadados calculados e agregados dos veículos
"""

from alembic import op
import sqlalchemy as sa
import os


# revision identifiers - auto-extraído do nome do arquivo
_filename = os.path.basename(__file__)
revision = _filename.split('_')[0]  # Pega '032' de '032_create_vehicle_meta_table.py'
down_revision = f"{int(revision) - 1:03d}"  # Calcula automaticamente: 032 -> 031
branch_labels = None
depends_on = None


def upgrade():
    """Cria a tabela vehicle_meta"""
    op.create_table(
        'vehicle_meta',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('vehicle_id', sa.Integer, sa.ForeignKey('vehicles.id', ondelete='CASCADE'), nullable=False, unique=True, comment='ID do veículo (único)'),
        sa.Column('current_km', sa.Integer, nullable=False, default=0, comment='Quilometragem atual (última informada)'),
        sa.Column('maintenance_type_id', sa.Integer, sa.ForeignKey('maintenance_types.id', ondelete='SET NULL'), nullable=True, comment='Tipo da próxima manutenção mais urgente'),
        sa.Column('due_at_km', sa.Integer, nullable=True, comment='Quilometragem da próxima manutenção'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('NOW()'), onupdate=sa.text('NOW()'), comment='Data da última atualização dos dados')
    )

    # Criar índices
    op.create_index('idx_vehicle_meta_vehicle_id', 'vehicle_meta', ['vehicle_id'])
    op.create_index('idx_vehicle_meta_maintenance_type_id', 'vehicle_meta', ['maintenance_type_id'])
    op.create_index('idx_vehicle_meta_due_at_km', 'vehicle_meta', ['due_at_km'])


def downgrade():
    """Remove a tabela vehicle_meta"""
    op.drop_index('idx_vehicle_meta_due_at_km', table_name='vehicle_meta')
    op.drop_index('idx_vehicle_meta_maintenance_type_id', table_name='vehicle_meta')
    op.drop_index('idx_vehicle_meta_vehicle_id', table_name='vehicle_meta')
    op.drop_table('vehicle_meta')
