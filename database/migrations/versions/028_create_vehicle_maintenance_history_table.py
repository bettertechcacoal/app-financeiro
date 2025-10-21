# -*- coding: utf-8 -*-
"""
Migration: Create vehicle_maintenance_history table
Tabela para armazenar histórico de manutenções realizadas
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '028'
down_revision = '027'
branch_labels = None
depends_on = None


def upgrade():
    """Cria a tabela vehicle_maintenance_history"""
    op.create_table(
        'vehicle_maintenance_history',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('vehicle_id', sa.Integer, sa.ForeignKey('vehicles.id', ondelete='CASCADE'), nullable=False, comment='ID do veículo'),
        sa.Column('type_id', sa.Integer, sa.ForeignKey('maintenance_types.id', ondelete='CASCADE'), nullable=False, comment='ID do tipo de manutenção'),
        sa.Column('description', sa.Text, nullable=True, comment='Detalhes da manutenção realizada'),
        sa.Column('km_performed', sa.Integer, nullable=False, comment='Quilometragem quando foi realizada'),
        sa.Column('performed_at', sa.DateTime, nullable=False, comment='Data em que a manutenção foi feita'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('NOW()'), comment='Data de criação do registro')
    )

    # Criar índices
    op.create_index('idx_vehicle_maintenance_history_vehicle_id', 'vehicle_maintenance_history', ['vehicle_id'])
    op.create_index('idx_vehicle_maintenance_history_type_id', 'vehicle_maintenance_history', ['type_id'])
    op.create_index('idx_vehicle_maintenance_history_performed_at', 'vehicle_maintenance_history', ['performed_at'])


def downgrade():
    """Remove a tabela vehicle_maintenance_history"""
    op.drop_index('idx_vehicle_maintenance_history_performed_at', table_name='vehicle_maintenance_history')
    op.drop_index('idx_vehicle_maintenance_history_type_id', table_name='vehicle_maintenance_history')
    op.drop_index('idx_vehicle_maintenance_history_vehicle_id', table_name='vehicle_maintenance_history')
    op.drop_table('vehicle_maintenance_history')
