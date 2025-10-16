# -*- coding: utf-8 -*-
"""
Migration: Create vehicle_issues table
Tabela para registrar problemas reportados nos veículos
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '028'
down_revision = '027'
branch_labels = None
depends_on = None


def upgrade():
    """Cria a tabela vehicle_issues"""
    op.create_table(
        'vehicle_issues',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('vehicle_id', sa.Integer, sa.ForeignKey('vehicles.id', ondelete='CASCADE'), nullable=False, comment='ID do veículo'),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, comment='ID do usuário que reportou'),
        sa.Column('description', sa.Text, nullable=False, comment='Descrição do problema'),
        sa.Column('status', sa.String(20), nullable=False, default='pendente', comment='Status: pendente, resolvido'),
        sa.Column('resolved_at', sa.DateTime, nullable=True, comment='Data de resolução do problema'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('NOW()'), comment='Data de criação do registro')
    )

    # Criar índices
    op.create_index('idx_vehicle_issues_vehicle_id', 'vehicle_issues', ['vehicle_id'])
    op.create_index('idx_vehicle_issues_status', 'vehicle_issues', ['status'])
    op.create_index('idx_vehicle_issues_created_at', 'vehicle_issues', ['created_at'])


def downgrade():
    """Remove a tabela vehicle_issues"""
    op.drop_index('idx_vehicle_issues_created_at', table_name='vehicle_issues')
    op.drop_index('idx_vehicle_issues_status', table_name='vehicle_issues')
    op.drop_index('idx_vehicle_issues_vehicle_id', table_name='vehicle_issues')
    op.drop_table('vehicle_issues')
