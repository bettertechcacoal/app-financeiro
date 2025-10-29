"""table vehicle_km_logs"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '025'
down_revision = '024'
branch_labels = None
depends_on = None


def upgrade():
    """Cria a tabela vehicle_km_logs"""
    op.create_table(
        'vehicle_km_logs',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('vehicle_id', sa.Integer, sa.ForeignKey('vehicles.id', ondelete='CASCADE'), nullable=False, comment='ID do veículo'),
        sa.Column('travel_id', sa.Integer, sa.ForeignKey('travels.id', ondelete='SET NULL'), nullable=True, comment='ID da viagem relacionada'),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, comment='ID do usuário que registrou'),
        sa.Column('previous_km', sa.Integer, nullable=False, comment='Quilometragem anterior'),
        sa.Column('current_km', sa.Integer, nullable=False, comment='Quilometragem atual'),
        sa.Column('km_traveled', sa.Integer, nullable=False, comment='Quilômetros rodados'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('NOW()'), comment='Data de criação')
    )

    # Criar índices
    op.create_index('idx_vehicle_km_logs_vehicle_id', 'vehicle_km_logs', ['vehicle_id'])
    op.create_index('idx_vehicle_km_logs_travel_id', 'vehicle_km_logs', ['travel_id'])
    op.create_index('idx_vehicle_km_logs_user_id', 'vehicle_km_logs', ['user_id'])


def downgrade():
    """Remove a tabela vehicle_km_logs"""
    # Usar IF EXISTS para evitar erros se a tabela não existir
    op.execute('DROP INDEX IF EXISTS idx_vehicle_km_logs_user_id')
    op.execute('DROP INDEX IF EXISTS idx_vehicle_km_logs_travel_id')
    op.execute('DROP INDEX IF EXISTS idx_vehicle_km_logs_vehicle_id')
    op.execute('DROP TABLE IF EXISTS vehicle_km_logs CASCADE')
