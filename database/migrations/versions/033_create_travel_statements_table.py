"""table travel_statements"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '033'
down_revision: Union[str, None] = '032'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Criar tabela travel_statements (o tipo enum será criado automaticamente pelo SQLAlchemy)
    op.create_table(
        'travel_statements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('payout_id', sa.Integer(), nullable=False),
        sa.Column('statement_content', sa.JSON(), nullable=True),
        sa.Column('status', sa.Enum('draft', 'submitted', 'returned', 'approved', name='statementstatus'), nullable=False, server_default='draft'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['payout_id'], ['travel_payouts.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('payout_id')
    )

    # Criar índices
    op.create_index('ix_travel_statements_payout_id', 'travel_statements', ['payout_id'])
    op.create_index('ix_travel_statements_status', 'travel_statements', ['status'])


def downgrade() -> None:
    # Remover índices
    op.drop_index('ix_travel_statements_status', 'travel_statements')
    op.drop_index('ix_travel_statements_payout_id', 'travel_statements')

    # Remover tabela (isso deve automaticamente dropar o enum se não houver outras dependências)
    op.drop_table('travel_statements')

    # Forçar remoção do enum type caso ainda exista
    op.execute('DROP TYPE IF EXISTS statementstatus CASCADE')
