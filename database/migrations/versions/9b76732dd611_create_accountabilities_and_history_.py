"""create_accountabilities_and_history_tables

Revision ID: 9b76732dd611
Revises: 032
Create Date: 2025-10-16 14:32:28.942694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b76732dd611'
down_revision: Union[str, None] = '032'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Criar ENUM type apenas se não existir
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE accountabilitystatus AS ENUM ('DRAFT', 'SUBMITTED', 'RETURNED', 'APPROVED');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # Criar tabela accountabilities
    op.create_table(
        'accountabilities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('payout_id', sa.Integer(), nullable=False),
        sa.Column('accommodation_expense', sa.Numeric(10, 2), server_default='0.00'),
        sa.Column('accommodation_receipt', sa.String(500)),
        sa.Column('food_expense', sa.Numeric(10, 2), server_default='0.00'),
        sa.Column('food_receipt', sa.String(500)),
        sa.Column('transport_expense', sa.Numeric(10, 2), server_default='0.00'),
        sa.Column('transport_receipt', sa.String(500)),
        sa.Column('fuel_expense', sa.Numeric(10, 2), server_default='0.00'),
        sa.Column('fuel_receipt', sa.String(500)),
        sa.Column('toll_expense', sa.Numeric(10, 2), server_default='0.00'),
        sa.Column('toll_receipt', sa.String(500)),
        sa.Column('parking_expense', sa.Numeric(10, 2), server_default='0.00'),
        sa.Column('parking_receipt', sa.String(500)),
        sa.Column('other_expense', sa.Numeric(10, 2), server_default='0.00'),
        sa.Column('other_receipt', sa.String(500)),
        sa.Column('other_description', sa.Text()),
        sa.Column('observations', sa.Text()),
        sa.Column('additional_data', sa.JSON()),
        sa.Column('status', sa.Enum('DRAFT', 'SUBMITTED', 'RETURNED', 'APPROVED', name='accountabilitystatus', create_type=False), nullable=False, server_default='DRAFT'),
        sa.Column('submitted_at', sa.DateTime(timezone=True)),
        sa.Column('reviewed_at', sa.DateTime(timezone=True)),
        sa.Column('approved_at', sa.DateTime(timezone=True)),
        sa.Column('reviewed_by', sa.Integer()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['payout_id'], ['travel_payouts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['reviewed_by'], ['users.id']),
        sa.UniqueConstraint('payout_id')
    )
    op.create_index('ix_accountabilities_payout_id', 'accountabilities', ['payout_id'])
    op.create_index('ix_accountabilities_status', 'accountabilities', ['status'])

    # Criar tabela accountability_history
    op.create_table(
        'accountability_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('accountability_id', sa.Integer(), nullable=False),
        sa.Column('from_status', sa.Enum('DRAFT', 'SUBMITTED', 'RETURNED', 'APPROVED', name='accountabilitystatus', create_type=False)),
        sa.Column('to_status', sa.Enum('DRAFT', 'SUBMITTED', 'RETURNED', 'APPROVED', name='accountabilitystatus', create_type=False), nullable=False),
        sa.Column('comment', sa.Text()),
        sa.Column('changed_by', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['accountability_id'], ['accountabilities.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['changed_by'], ['users.id'])
    )
    op.create_index('ix_accountability_history_accountability_id', 'accountability_history', ['accountability_id'])


def downgrade() -> None:
    # Remover tabelas na ordem inversa
    op.drop_index('ix_accountability_history_accountability_id', 'accountability_history')
    op.drop_table('accountability_history')

    op.drop_index('ix_accountabilities_status', 'accountabilities')
    op.drop_index('ix_accountabilities_payout_id', 'accountabilities')
    op.drop_table('accountabilities')

    # Remover enum type
    op.execute('DROP TYPE IF EXISTS accountabilitystatus')
