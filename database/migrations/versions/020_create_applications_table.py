"""table applications"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '020'
down_revision: Union[str, None] = '019'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria tabela applications (aplicações/módulos)"""
    op.create_table(
        'applications',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False, unique=True),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),  # Ex: APICE, WEB, AISE, OXY, Portal
        sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar índices
    op.create_index('idx_applications_name', 'applications', ['name'])
    op.create_index('idx_applications_category', 'applications', ['category'])
    op.create_index('idx_applications_is_active', 'applications', ['is_active'])


def downgrade() -> None:
    """Remove tabela applications"""
    op.drop_index('idx_applications_is_active', table_name='applications')
    op.drop_index('idx_applications_category', table_name='applications')
    op.drop_index('idx_applications_name', table_name='applications')
    op.drop_table('applications')
