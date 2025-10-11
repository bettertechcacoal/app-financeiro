"""create organizations table

Revision ID: 007
Revises: 006
Create Date: 2025-10-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '007'
down_revision: Union[str, None] = '006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria tabela organizations"""
    op.create_table(
        'organizations',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('business_name', sa.String(length=255), nullable=False),
        sa.Column('person_type', sa.String(length=20), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Remove tabela organizations"""
    op.drop_table('organizations')
