"""create travel_passengers table

Revision ID: 012
Revises: 011
Create Date: 2025-10-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '012'
down_revision: Union[str, None] = '011'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria tabela travel_passengers - relacionamento many-to-many entre travels e users"""
    op.create_table(
        'travel_passengers',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('travel_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['travel_id'], ['travels.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('travel_id', 'user_id', name='uq_travel_passenger')
    )

    # Criar índices para melhor performance
    op.create_index('idx_travel_passengers_travel_id', 'travel_passengers', ['travel_id'])
    op.create_index('idx_travel_passengers_user_id', 'travel_passengers', ['user_id'])


def downgrade() -> None:
    """Remove tabela travel_passengers"""
    op.drop_index('idx_travel_passengers_user_id', table_name='travel_passengers')
    op.drop_index('idx_travel_passengers_travel_id', table_name='travel_passengers')
    op.drop_table('travel_passengers')
