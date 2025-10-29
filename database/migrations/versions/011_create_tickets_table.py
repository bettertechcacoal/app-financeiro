"""table tickets"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '011'
down_revision: Union[str, None] = '010'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria tabela tickets"""
    op.create_table(
        'tickets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('subject', sa.String(length=500), nullable=True),
        sa.Column('status', sa.String(length=100), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('service_full', sa.String(length=500), nullable=True),
        sa.Column('organization_name', sa.String(length=255), nullable=True),
        sa.Column('client_name', sa.String(length=255), nullable=True),
        sa.Column('owner_name', sa.String(length=255), nullable=True),
        sa.Column('created_by_name', sa.String(length=255), nullable=True),
        sa.Column('created_by_email', sa.String(length=255), nullable=True),
        sa.Column('created_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('resolved_in', sa.DateTime(timezone=True), nullable=True),
        sa.Column('closed_in', sa.DateTime(timezone=True), nullable=True),
        sa.Column('custom_field_module', sa.String(length=255), nullable=True),
        sa.Column('synced_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Remove tabela tickets"""
    op.drop_table('tickets')
