"""create application_ticket_module junction table"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '035'
down_revision: Union[str, None] = '034'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Criar tabela de associação application_ticket_module
    op.create_table(
        'application_ticket_module',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('application_id', sa.Integer(), nullable=False),
        sa.Column('ticket_module_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['application_id'], ['applications.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['ticket_module_id'], ['tickets_modules.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('application_id', 'ticket_module_id', name='uq_application_ticket_module')
    )

    # Criar índices para melhor performance nas consultas
    op.create_index('ix_application_ticket_module_application_id', 'application_ticket_module', ['application_id'])
    op.create_index('ix_application_ticket_module_ticket_module_id', 'application_ticket_module', ['ticket_module_id'])


def downgrade() -> None:
    # Remover índices
    op.drop_index('ix_application_ticket_module_ticket_module_id', 'application_ticket_module')
    op.drop_index('ix_application_ticket_module_application_id', 'application_ticket_module')

    # Remover tabela
    op.drop_table('application_ticket_module')
