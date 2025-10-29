"""table ticket_sync_logs"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '010'
down_revision: Union[str, None] = '009'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria tabela ticket_sync_logs"""
    op.create_table(
        'ticket_sync_logs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('sync_type', sa.String(length=50), nullable=False),
        sa.Column('total', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('synced', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('updated', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('errors', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('synced_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Remove tabela ticket_sync_logs"""
    op.drop_table('ticket_sync_logs')
