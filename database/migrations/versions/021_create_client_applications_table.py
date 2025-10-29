"""table client_applications"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '021'
down_revision: Union[str, None] = '020'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria tabela client_applications (associação N:N entre clients e applications)"""
    op.create_table(
        'client_applications',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('application_id', sa.Integer(), nullable=False),
        sa.Column('cod_elotech', sa.String(length=15), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['application_id'], ['applications.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('client_id', 'application_id', name='unique_client_application')
    )

    # Criar índices
    op.create_index('idx_client_applications_client_id', 'client_applications', ['client_id'])
    op.create_index('idx_client_applications_application_id', 'client_applications', ['application_id'])
    op.create_index('idx_client_applications_is_active', 'client_applications', ['is_active'])


def downgrade() -> None:
    """Remove tabela client_applications"""
    op.drop_index('idx_client_applications_is_active', table_name='client_applications')
    op.drop_index('idx_client_applications_application_id', table_name='client_applications')
    op.drop_index('idx_client_applications_client_id', table_name='client_applications')
    op.drop_table('client_applications')
