"""table travels"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '006'
down_revision: Union[str, None] = '005'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria tabela travels"""
    op.create_table(
        'travels',
        # ID único da viagem
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        # ID do usuário motorista/viajante
        sa.Column('driver_user_id', sa.Integer(), nullable=False),
        # ID da cidade de destino
        sa.Column('city_id', sa.Integer(), nullable=False),
        # Motivo/propósito da viagem
        sa.Column('purpose', sa.String(length=255), nullable=False),
        # Data e hora de saída
        sa.Column('departure_date', sa.DateTime(timezone=True), nullable=False),
        # Data e hora de retorno
        sa.Column('return_date', sa.DateTime(timezone=True), nullable=False),
        # Indica se necessita reserva de veículo da frota
        sa.Column('needs_vehicle', sa.Boolean(), nullable=False, server_default='false'),
        # ID do usuário que criou o registro
        sa.Column('record_user_id', sa.Integer(), nullable=False),
        # Status atual da viagem (pending, approved, in_progress, completed, cancelled)
        sa.Column('status', sa.Enum('pending', 'approved', 'in_progress', 'completed', 'cancelled', name='travelstatus'), nullable=False),
        # ID do usuário que aprovou a viagem
        sa.Column('approved_by', sa.Integer(), nullable=True),
        # Data e hora da aprovação
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        # Observações gerais da viagem
        sa.Column('notes', sa.Text(), nullable=True),
        # Notas administrativas (visível apenas para gestores)
        sa.Column('admin_notes', sa.Text(), nullable=True),
        # Data de criação do registro
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        # Data da última atualização
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        # Chaves estrangeiras
        sa.ForeignKeyConstraint(['driver_user_id'], ['users.id'], name='fk_travels_driver_user'),
        sa.ForeignKeyConstraint(['record_user_id'], ['users.id'], name='fk_travels_record_user'),
        sa.ForeignKeyConstraint(['city_id'], ['cities.id'], name='fk_travels_city'),
        sa.ForeignKeyConstraint(['approved_by'], ['users.id'], name='fk_travels_approved_by'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Remove tabela travels"""
    op.drop_table('travels')

    # Remover o tipo enum
    sa.Enum(name='travelstatus').drop(op.get_bind(), checkfirst=True)
