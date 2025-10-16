"""create travels table

Revision ID: 006
Revises: 005
Create Date: 2025-10-11

"""
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
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='ID único da viagem'),
        sa.Column('driver_user_id', sa.Integer(), nullable=False, comment='ID do usuário motorista/viajante'),
        sa.Column('city_id', sa.Integer(), nullable=False, comment='ID da cidade de destino'),
        sa.Column('purpose', sa.String(length=255), nullable=False, comment='Motivo/propósito da viagem'),
        sa.Column('description', sa.Text(), nullable=True, comment='Descrição detalhada da viagem'),
        sa.Column('departure_date', sa.DateTime(timezone=True), nullable=False, comment='Data e hora de saída'),
        sa.Column('return_date', sa.DateTime(timezone=True), nullable=False, comment='Data e hora de retorno'),
        sa.Column('needs_vehicle', sa.Boolean(), nullable=False, server_default='false', comment='Indica se necessita reserva de veículo da frota'),
        sa.Column('record_user_id', sa.Integer(), nullable=False, comment='ID do usuário que criou o registro'),
        sa.Column('status', sa.Enum('PENDING', 'APPROVED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', name='travelstatus'), nullable=False, comment='Status atual da viagem'),
        sa.Column('approved_by', sa.Integer(), nullable=True, comment='ID do usuário que aprovou a viagem'),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True, comment='Data e hora da aprovação'),
        sa.Column('notes', sa.Text(), nullable=True, comment='Observações gerais da viagem'),
        sa.Column('admin_notes', sa.Text(), nullable=True, comment='Notas administrativas (visível apenas para gestores)'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Data de criação do registro'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Data da última atualização'),
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
