"""add payout_history column to travel_payouts"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Session
import json


# revision identifiers, used by Alembic.
revision: str = '036'
down_revision: Union[str, None] = '035'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Adiciona coluna payout_history para histórico de lançamentos em JSONB"""
    # Adicionar a coluna
    op.add_column('travel_payouts', sa.Column('payout_history', JSONB(), nullable=True))

    # Popular histórico para registros existentes
    connection = op.get_bind()
    session = Session(bind=connection)

    try:
        # Buscar todos os payouts existentes que têm amount > 0 e payout_history vazio/nulo
        # Inclui o approved_by da viagem para identificar quem criou o lançamento
        result = connection.execute(
            sa.text("""
                SELECT tp.id, tp.amount, tp.created_at, t.approved_by
                FROM travel_payouts tp
                JOIN travels t ON t.id = tp.travel_id
                WHERE tp.amount > 0 AND (tp.payout_history IS NULL OR tp.payout_history = '[]'::jsonb)
            """)
        )

        for row in result:
            payout_id = row[0]
            amount = float(row[1]) if row[1] else 0
            created_at = row[2]
            approved_by = row[3]

            if amount > 0:
                # Criar histórico inicial com os dados existentes
                history = [{
                    'amount': amount,
                    'date': created_at.strftime('%Y-%m-%d') if created_at else None,
                    'observation': '',
                    'created_by': approved_by,
                    'created_at': created_at.isoformat() if created_at else None,
                    'status': 'launched'
                }]

                # Atualizar o registro com o histórico
                connection.execute(
                    sa.text("""
                        UPDATE travel_payouts
                        SET payout_history = :history
                        WHERE id = :id
                    """),
                    {'history': json.dumps(history), 'id': payout_id}
                )

        session.commit()
        print(f"Migration 036: Histórico de payouts populado com sucesso.")

    except Exception as e:
        session.rollback()
        print(f"Migration 036: Erro ao popular histórico: {e}")
        raise


def downgrade() -> None:
    """Remove coluna payout_history"""
    op.drop_column('travel_payouts', 'payout_history')
