"""create travels system tables

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
    """Cria tabelas states, cities, users e travels"""

    # Tabela states
    op.create_table(
        'states',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('uf', sa.String(length=2), nullable=False),
        sa.Column('ibge_code', sa.String(length=2), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_states_uf', 'states', ['uf'], unique=True)
    op.create_index('ix_states_ibge_code', 'states', ['ibge_code'], unique=True)

    # Tabela cities
    op.create_table(
        'cities',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('ibge_code', sa.String(length=7), nullable=False),
        sa.Column('state_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['state_id'], ['states.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_cities_ibge_code', 'cities', ['ibge_code'], unique=True)

    # Tabela users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('cpf', sa.String(length=14), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('avatar', sa.String(length=255), nullable=True),
        sa.Column('user_group_id', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('email_verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_group_id'], ['user_groups.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_cpf', 'users', ['cpf'], unique=True)

    # Tabela travels
    op.create_table(
        'travels',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('city_id', sa.Integer(), nullable=False),
        sa.Column('purpose', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('departure_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('return_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'APPROVED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', name='travelstatus'), nullable=False),
        sa.Column('approved_by', sa.Integer(), nullable=True),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('admin_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['city_id'], ['cities.id']),
        sa.ForeignKeyConstraint(['approved_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Remove tabelas travels, users, cities e states"""
    op.drop_table('travels')
    op.drop_index('ix_users_cpf', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_cities_ibge_code', table_name='cities')
    op.drop_table('cities')
    op.drop_index('ix_states_ibge_code', table_name='states')
    op.drop_index('ix_states_uf', table_name='states')
    op.drop_table('states')

    # Remover o tipo enum
    sa.Enum(name='travelstatus').drop(op.get_bind(), checkfirst=True)
