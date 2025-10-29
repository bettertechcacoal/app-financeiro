"""table vehicle_maintenance_configs"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '030'
down_revision = '029'
branch_labels = None
depends_on = None


def upgrade():
    """Cria a tabela vehicle_maintenance_configs"""
    op.create_table(
        'vehicle_maintenance_configs',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('vehicle_id', sa.Integer, sa.ForeignKey('vehicles.id', ondelete='CASCADE'), nullable=False, comment='ID do veículo'),
        sa.Column('maintenance_type_id', sa.Integer, sa.ForeignKey('maintenance_types.id', ondelete='CASCADE'), nullable=False, comment='ID do tipo de manutenção'),
        sa.Column('km_interval', sa.Integer, nullable=False, comment='Intervalo em KM entre manutenções'),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True, comment='Configuração ativa'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('NOW()'), comment='Data de criação'),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('NOW()'), onupdate=sa.text('NOW()'), comment='Data de atualização')
    )

    # Criar índices
    op.create_index('idx_vehicle_maintenance_configs_vehicle_id', 'vehicle_maintenance_configs', ['vehicle_id'])
    op.create_index('idx_vehicle_maintenance_configs_maintenance_type_id', 'vehicle_maintenance_configs', ['maintenance_type_id'])
    op.create_index('idx_vehicle_maintenance_configs_is_active', 'vehicle_maintenance_configs', ['is_active'])

    # Criar unique constraint para evitar duplicação de configuração
    op.create_unique_constraint(
        'uq_vehicle_maintenance_config',
        'vehicle_maintenance_configs',
        ['vehicle_id', 'maintenance_type_id']
    )


def downgrade():
    """Remove a tabela vehicle_maintenance_configs"""
    op.drop_constraint('uq_vehicle_maintenance_config', 'vehicle_maintenance_configs', type_='unique')
    op.drop_index('idx_vehicle_maintenance_configs_is_active', table_name='vehicle_maintenance_configs')
    op.drop_index('idx_vehicle_maintenance_configs_maintenance_type_id', table_name='vehicle_maintenance_configs')
    op.drop_index('idx_vehicle_maintenance_configs_vehicle_id', table_name='vehicle_maintenance_configs')
    op.drop_table('vehicle_maintenance_configs')
