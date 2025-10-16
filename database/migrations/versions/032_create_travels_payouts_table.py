"""create travel_payouts table

Revision ID: 032
Revises: 031
Create Date: 2025-10-15

"""
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
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('travel_id', sa.Integer(), nullable=False),
        sa.Column('member_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['travel_id'], ['travels.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['member_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar índices para melhor performance
    op.create_index('idx_travel_payouts_travel_id', 'travel_payouts', ['travel_id'])
    op.create_index('idx_travel_payouts_member_id', 'travel_payouts', ['member_id'])
    op.create_index('idx_travel_payouts_status', 'travel_payouts', ['status'])


def downgrade() -> None:
    """Remove tabela travel_payouts"""
    op.drop_index('idx_travel_payouts_status', table_name='travel_payouts')
    op.drop_index('idx_travel_payouts_member_id', table_name='travel_payouts')
    op.drop_index('idx_travel_payouts_travel_id', table_name='travel_payouts')
    op.drop_table('travel_payouts')
