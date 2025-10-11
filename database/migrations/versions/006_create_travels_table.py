"""create travels table

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
    """Cria tabela travels"""
    op.create_table(
        'travels',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('city_id', sa.Integer(), nullable=False),
        sa.Column('purpose', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('departure_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('return_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'APPROVED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', name='travelstatus'), nullable=False),
        sa.Column('approved_by', sa.Integer(), nullable=True),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('admin_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['city_id'], ['cities.id']),
        sa.ForeignKeyConstraint(['approved_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Remove tabela travels"""
    op.drop_table('travels')

    # Remover o tipo enum
    sa.Enum(name='travelstatus').drop(op.get_bind(), checkfirst=True)
