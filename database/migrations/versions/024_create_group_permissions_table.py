"""create group_permissions table

Revision ID: 024
Revises: 023
Create Date: 2024-10-13

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = '024'
down_revision = '023'
branch_labels = None
depends_on = None


def upgrade():
    """Cria a tabela group_permissions (pivot table)"""
    op.create_table(
        'group_permissions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('permission_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
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
