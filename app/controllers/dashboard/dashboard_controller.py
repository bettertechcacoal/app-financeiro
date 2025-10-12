# -*- coding: utf-8 -*-
from flask import render_template, session
from app.models.database import get_db
from app.models.travel import Travel, TravelStatus
from app.models.note import Note
from sqlalchemy import desc


def dashboard():
    """Controller do dashboard principal"""
    user_id = session.get('user_id')
    user_name = session.get('user_name', 'Usuário')

    db = get_db()

    # Contar viagens pendentes
    pending_travels_count = db.query(Travel).filter_by(status=TravelStatus.PENDING).count()

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
        notes=notes,
        total_notes=total_notes
    )
