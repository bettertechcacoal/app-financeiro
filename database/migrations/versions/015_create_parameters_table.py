"""table parameters"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '015'
down_revision: Union[str, None] = '014'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Criar tabela parameters"""

    # Criar o tipo ENUM do PostgreSQL
    parameter_type_enum = postgresql.ENUM('TEXT', 'CHECKBOX', 'SELECT', 'JSON', name='parametertype', create_type=True)
    parameter_type_enum.create(op.get_bind(), checkfirst=True)

    # Criar tabela parameters
    op.create_table(
        'parameters',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('parameter', sa.String(length=100), nullable=False),
        sa.Column('type', postgresql.ENUM('TEXT', 'CHECKBOX', 'SELECT', 'JSON', name='parametertype', create_type=False), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=False),
        sa.Column('value', sa.Text(), nullable=True),
        sa.Column('options', sa.Text(), nullable=True),
        sa.Column('group_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('parameter'),
        sa.ForeignKeyConstraint(['group_id'], ['parameter_groups.id'], ondelete='SET NULL')
    )


def downgrade() -> None:
    """Remover tabela parameters"""
    op.drop_table('parameters')
    op.execute('DROP TYPE IF EXISTS parametertype')
