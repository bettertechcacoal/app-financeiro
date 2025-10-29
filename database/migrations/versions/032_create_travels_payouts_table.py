"""table travel_payouts"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '032'
down_revision: Union[str, None] = '031'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria tabela travel_payouts - controle de repasses financeiros por participante"""
    op.create_table(
        'travel_payouts',
        # ID único do registro de repasse
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        # ID da viagem à qual o repasse está vinculado
        sa.Column('travel_id', sa.Integer(), nullable=False),
        # ID do membro/usuário que receberá o repasse financeiro
        sa.Column('member_id', sa.Integer(), nullable=False),
        # Valor monetário do repasse em formato decimal (até 99.999.999,99)
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        # Data e hora de criação do registro
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        # Data e hora da última atualização do registro
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        # Chave estrangeira - deleta repasse se a viagem for deletada
        sa.ForeignKeyConstraint(['travel_id'], ['travels.id'], ondelete='CASCADE'),
        # Chave estrangeira - deleta repasse se o usuário for deletado
        sa.ForeignKeyConstraint(['member_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar índices para melhor performance nas consultas
    op.create_index('idx_travel_payouts_travel_id', 'travel_payouts', ['travel_id'])
    op.create_index('idx_travel_payouts_member_id', 'travel_payouts', ['member_id'])


def downgrade() -> None:
    """Remove tabela travel_payouts"""
    op.drop_index('idx_travel_payouts_member_id', table_name='travel_payouts')
    op.drop_index('idx_travel_payouts_travel_id', table_name='travel_payouts')

    # Usar CASCADE para dropar dependências
    op.execute('DROP TABLE IF EXISTS travel_payouts CASCADE')
