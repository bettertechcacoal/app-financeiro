# -*- coding: utf-8 -*-
from flask import render_template, session
from app.models.database import get_db
from app.models.travel import Travel, TravelStatus
from app.models.travel_payout import TravelPayout
from app.models.travel_statement import TravelStatement, StatementStatus
from app.models.note import Note
from sqlalchemy import desc, or_, and_
from datetime import datetime


def dashboard():
    """Controller do dashboard principal"""
    user_id = session.get('user_id')
    user_name = session.get('user_name', 'Usuário')

    db = get_db()

    # Contar viagens pendentes
    pending_travels_count = db.query(Travel).filter_by(status=TravelStatus.PENDING).count()

    # Contar travel_payouts que precisam de atenção
    pending_payouts_count = 0
    if user_id:
        # Verificar se usuário tem permissão de analista
        from app.utils.permissions_helper import user_has_permission
        can_review_all = user_has_permission('financial_review_accountability')

        if not can_review_all:
            # Colaborador: conta repasses que ainda não enviou ou que foram devolvidos
            pending_payouts_count = db.query(TravelPayout)\
                .outerjoin(TravelStatement, TravelPayout.id == TravelStatement.payout_id)\
                .filter(TravelPayout.member_id == user_id)\
                .filter(
                    or_(
                        # Ainda não enviou (sem prestação ou status draft)
                        TravelStatement.status.is_(None),
                        TravelStatement.status == StatementStatus.DRAFT,
                        # Foi devolvido para correção
                        TravelStatement.status == StatementStatus.RETURNED
                    )
                ).count()
        else:
            # Analista: usa mesmas condições da listagem, mas exclui aprovados
            today = datetime.now().date()

            # Buscar payouts usando mesma lógica da listagem (excluindo aprovados)
            query = db.query(TravelPayout)\
                .outerjoin(TravelStatement, TravelPayout.id == TravelStatement.payout_id)\
                .join(Travel, TravelPayout.travel_id == Travel.id)\
                .filter(
                    and_(
                        # Excluir aprovados
                        or_(
                            TravelStatement.status.is_(None),
                            TravelStatement.status != StatementStatus.APPROVED
                        ),
                        # Condições da listagem
                        or_(
                            # Seus próprios repasses
                            TravelPayout.member_id == user_id,
                            # Repasses já enviados
                            TravelStatement.status == StatementStatus.SUBMITTED,
                            # Repasses cuja data de retorno já passou
                            and_(
                                Travel.return_date.isnot(None),
                                Travel.return_date < today
                            )
                        )
                    )
                )

            pending_payouts_count = query.count()

    # Buscar notes do usuário (limite de 5 para dashboard)
    notes = []
    total_notes = 0
    if user_id:
        notes = db.query(Note).filter_by(user_id=user_id).order_by(desc(Note.created_at)).limit(5).all()
        total_notes = db.query(Note).filter_by(user_id=user_id).count()

    return render_template(
        'pages/dashboard.html',
        user_name=user_name,
        pending_travels_count=pending_travels_count,
        pending_payouts_count=pending_payouts_count,
        notes=notes,
        total_notes=total_notes
    )
