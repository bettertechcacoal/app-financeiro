"""create notes table

Revision ID: 017
Revises: 016
Create Date: 2025-01-11

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '017'
down_revision: Union[str, None] = '016'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Criar tabela notes"""

    # Create PostgreSQL ENUM type for note colors
    note_color_enum = postgresql.ENUM('YELLOW', 'PINK', 'GREEN', 'BLUE', 'PURPLE', name='notecolor', create_type=True)
    note_color_enum.create(op.get_bind(), checkfirst=True)

    # Create notes table
    op.create_table(
        'notes',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('color', postgresql.ENUM('YELLOW', 'PINK', 'GREEN', 'BLUE', 'PURPLE', name='notecolor', create_type=False), nullable=False, server_default='YELLOW'),
        sa.Column('icon', sa.String(length=50), nullable=True, server_default='fa-sticky-note'),
        sa.Column('label', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )


def downgrade() -> None:
    """Remover tabela notes"""
    op.drop_table('notes')

    # Drop ENUM type
    note_color_enum = postgresql.ENUM(name='notecolor')
    note_color_enum.drop(op.get_bind(), checkfirst=True)
