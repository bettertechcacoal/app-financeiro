"""table vehicle_travel_history"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '027'
down_revision = '026'
branch_labels = None
depends_on = None


def upgrade():
    """Cria a tabela vehicle_travel_history"""
    op.create_table(
        'vehicle_travel_history',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('vehicle_id', sa.Integer, sa.ForeignKey('vehicles.id', ondelete='CASCADE'), nullable=False, comment='ID do veículo'),
        sa.Column('travel_id', sa.Integer, sa.ForeignKey('travels.id', ondelete='SET NULL'), nullable=True, comment='ID da viagem relacionada'),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, comment='ID do usuário que registrou'),
        sa.Column('previous_km', sa.Integer, nullable=False, comment='Quilometragem anterior'),
        sa.Column('current_km', sa.Integer, nullable=False, comment='Quilometragem atual'),
        sa.Column('km_traveled', sa.Integer, nullable=False, comment='Quilômetros rodados (current_km - previous_km)'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('NOW()'), comment='Data de criação do registro')
    )

    # Criar índices
    op.create_index('idx_vehicle_travel_history_vehicle_id', 'vehicle_travel_history', ['vehicle_id'])
    op.create_index('idx_vehicle_travel_history_travel_id', 'vehicle_travel_history', ['travel_id'])
    op.create_index('idx_vehicle_travel_history_user_id', 'vehicle_travel_history', ['user_id'])
    op.create_index('idx_vehicle_travel_history_created_at', 'vehicle_travel_history', ['created_at'])


def downgrade():
    """Remove a tabela vehicle_travel_history"""
    op.drop_index('idx_vehicle_travel_history_created_at', table_name='vehicle_travel_history')
    op.drop_index('idx_vehicle_travel_history_user_id', table_name='vehicle_travel_history')
    op.drop_index('idx_vehicle_travel_history_travel_id', table_name='vehicle_travel_history')
    op.drop_index('idx_vehicle_travel_history_vehicle_id', table_name='vehicle_travel_history')
    op.drop_table('vehicle_travel_history')
