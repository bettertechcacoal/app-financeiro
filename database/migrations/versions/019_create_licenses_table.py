# -*- coding: utf-8 -*-
"""
Cria tabela de licenças/senhas dos clientes (dados dos TXT de senhas)
"""
from alembic import op
import sqlalchemy as sa


revision = '019'
down_revision = '018'
branch_labels = None
depends_on = None


def upgrade():
    # Dropar tabela antiga se existir
    op.execute('DROP TABLE IF EXISTS licenses CASCADE')

    # Criar nova tabela de licenças
    op.create_table(
        'licenses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('client_code', sa.String(50), nullable=False),
        sa.Column('client_name', sa.String(255), nullable=False),
        sa.Column('license_date', sa.Date(), nullable=False),
        sa.Column('module_code', sa.String(200), nullable=False),
        sa.Column('password', sa.String(100), nullable=False)
    )

    # Criar índices para consultas rápidas
    op.create_index('idx_licenses_client_code', 'licenses', ['client_code'])
    op.create_index('idx_licenses_license_date', 'licenses', ['license_date'])
    op.create_index('idx_licenses_client_date', 'licenses', ['client_code', 'license_date'])


def downgrade():
    # Usar DROP IF EXISTS para evitar erros se os índices não existirem
    op.execute('DROP INDEX IF EXISTS idx_licenses_client_date')
    op.execute('DROP INDEX IF EXISTS idx_licenses_license_date')
    op.execute('DROP INDEX IF EXISTS idx_licenses_client_code')
    op.drop_table('licenses')
