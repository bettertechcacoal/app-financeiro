"""create permissions table

Revision ID: 023
Revises: 022
Create Date: 2024-10-13

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = '023'
down_revision = '022'
branch_labels = None
depends_on = None


def upgrade():
    """Cria a tabela permissions"""
    op.create_table(
        'permissions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('module', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar índice único para o slug
    op.create_index('ix_permissions_slug', 'permissions', ['slug'], unique=True)


def downgrade():
    """Remove a tabela permissions"""
    op.drop_index('ix_permissions_slug', table_name='permissions')
    op.drop_table('permissions')
