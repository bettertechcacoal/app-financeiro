"""create user_groups table

Revision ID: 003
Revises: 002
Create Date: 2025-10-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria tabela user_groups (pivot)"""
    op.create_table(
        'user_groups',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'group_id', name='unique_user_group')
    )

    # Criar índices
    op.create_index('idx_user_groups_user_id', 'user_groups', ['user_id'])
    op.create_index('idx_user_groups_group_id', 'user_groups', ['group_id'])


def downgrade() -> None:
    """Remove tabela user_groups"""
    op.drop_index('idx_user_groups_group_id', table_name='user_groups')
    op.drop_index('idx_user_groups_user_id', table_name='user_groups')
    op.drop_table('user_groups')
