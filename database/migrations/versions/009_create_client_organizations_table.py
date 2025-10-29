"""table client_organizations"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '009'
down_revision: Union[str, None] = '008'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria tabela client_organizations (pivot)"""
    op.create_table(
        'client_organizations',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('organization_id', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('client_id', 'organization_id', name='unique_client_organization')
    )

    # Criar índices
    op.create_index('idx_client_organizations_client_id', 'client_organizations', ['client_id'])
    op.create_index('idx_client_organizations_organization_id', 'client_organizations', ['organization_id'])


def downgrade() -> None:
    """Remove tabela client_organizations"""
    op.drop_index('idx_client_organizations_organization_id', table_name='client_organizations')
    op.drop_index('idx_client_organizations_client_id', table_name='client_organizations')
    op.drop_table('client_organizations')
