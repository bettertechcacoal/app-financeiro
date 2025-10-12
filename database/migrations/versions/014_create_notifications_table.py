"""create notifications table

Revision ID: 014
Revises: 013
Create Date: 2025-10-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '014'
down_revision: Union[str, None] = '013'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria tabela notifications"""
    conn = op.get_bind()

    # Criar o tipo ENUM se não existir
    conn.execute(sa.text("""
        DO $$ BEGIN
            CREATE TYPE notificationtype AS ENUM ('INFO', 'SUCCESS', 'WARNING', 'ERROR', 'TRAVEL', 'TICKET', 'SYSTEM');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """))

    # Criar tabela usando SQL nativo
    conn.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS notifications (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            title VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            type notificationtype NOT NULL DEFAULT 'INFO',
            action_url VARCHAR(500),
            action_text VARCHAR(100),
            is_read BOOLEAN NOT NULL DEFAULT false,
            read_at TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            CONSTRAINT fk_notifications_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """))

    # Criar índices para melhor performance
    conn.execute(sa.text("CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id)"))
    conn.execute(sa.text("CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read)"))
    conn.execute(sa.text("CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at)"))


def downgrade() -> None:
    """Remove tabela notifications"""
    op.drop_index('idx_notifications_created_at', table_name='notifications')
    op.drop_index('idx_notifications_is_read', table_name='notifications')
    op.drop_index('idx_notifications_user_id', table_name='notifications')
    op.drop_table('notifications')
    op.execute('DROP TYPE notificationtype')
