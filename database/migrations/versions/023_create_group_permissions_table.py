"""table group_permissions"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '023'
down_revision: Union[str, None] = '022'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria a tabela group_permissions (pivot table)"""
    op.create_table(
        'group_permissions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('permission_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar índice único para evitar duplicatas (group_id + permission_id)
    op.create_index('ix_group_permissions_unique', 'group_permissions', ['group_id', 'permission_id'], unique=True)


def downgrade():
    """Remove a tabela group_permissions"""
    op.drop_index('ix_group_permissions_unique', table_name='group_permissions')
    op.drop_table('group_permissions')
