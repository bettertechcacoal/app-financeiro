# -*- coding: utf-8 -*-
from flask import render_template, session
from app.models.database import get_db
from app.models.travel import Travel, TravelStatus


def dashboard():
    """Controller do dashboard principal"""
    user_name = session.get('user_name', 'Usuário')

    # Contar viagens pendentes
    db = get_db()
    pending_travels_count = db.query(Travel).filter_by(status=TravelStatus.PENDING).count()

    return render_template('pages/dashboard.html', user_name=user_name, pending_travels_count=pending_travels_count)
