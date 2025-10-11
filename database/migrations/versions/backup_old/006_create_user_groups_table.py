"""create user_groups table

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
    """Cria tabela user_groups"""
    op.create_table(
        'user_groups',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('color', sa.String(length=20), nullable=True, server_default='#3b82f6'),
        sa.Column('icon', sa.String(length=50), nullable=True, server_default='fa-users'),
        sa.Column('permissions', sa.Text(), nullable=True),
        sa.Column('hierarchy_level', sa.Integer(), nullable=True, server_default='99'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar índices
    op.create_index('ix_user_groups_slug', 'user_groups', ['slug'], unique=True)


def downgrade() -> None:
    """Remove tabela user_groups"""
    op.drop_index('ix_user_groups_slug', table_name='user_groups')
    op.drop_table('user_groups')
