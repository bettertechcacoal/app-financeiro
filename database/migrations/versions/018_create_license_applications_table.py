"""table license_applications"""
from alembic import op
import sqlalchemy as sa


revision = '018'
down_revision = '017'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'license_applications',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('code', sa.String(10), unique=True, nullable=False),  # Código do módulo (002, 003, etc.)
        sa.Column('name', sa.String(200), nullable=False)  # Nome do módulo (APICE - Orçamento, etc.)
    )

    # Índice para busca rápida por código
    op.create_index('idx_license_applications_code', 'license_applications', ['code'])


def downgrade():
    op.execute('DROP INDEX IF EXISTS idx_license_applications_code')
    op.execute('DROP TABLE IF EXISTS license_applications')
