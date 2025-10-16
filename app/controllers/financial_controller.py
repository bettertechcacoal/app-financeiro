# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, session
from app.models.database import SessionLocal
from app.models.travel_payout import TravelPayout, PayoutStatus
from app.models.travel import Travel
from app.models.user import User
from app.models.city import City
from app.models.state import State
from sqlalchemy.orm import joinedload


def financial_accountability(payout_id):
    """Exibe tela de prestação de contas (wizard)"""
    try:
        db = SessionLocal()

        # Obter ID do usuário logado
        user_id = session.get('user_id')

        if not user_id:
            flash('Usuário não autenticado', 'error')
            return redirect(url_for('auth.login'))

        # Buscar o payout do usuário logado
        payout = db.query(TravelPayout)\
            .filter_by(id=payout_id, member_id=user_id)\
            .join(Travel)\
            .options(
                joinedload(TravelPayout.travel).joinedload(Travel.city).joinedload(City.state),
                joinedload(TravelPayout.travel).joinedload(Travel.user)
            )\
            .first()

        if not payout:
            flash('Repasse não encontrado ou você não tem permissão para acessá-lo', 'error')
            return redirect(url_for('admin.financial_payouts_list'))

        # Verificar se o payout está pendente
        if payout.status != PayoutStatus.PENDING:
            flash('Este repasse já foi processado', 'warning')
            return redirect(url_for('admin.financial_payouts_list'))

        payout_data = payout.to_dict()

        # Adicionar informações da viagem
        if payout.travel:
            payout_data['travel_info'] = {
                'id': payout.travel.id,
                'purpose': payout.travel.purpose,
                'departure_date': payout.travel.departure_date.isoformat() if payout.travel.departure_date else None,
                'return_date': payout.travel.return_date.isoformat() if payout.travel.return_date else None,
                'status': payout.travel.status.value if payout.travel.status else None,
                'city': payout.travel.city.to_dict() if payout.travel.city else None,
                'user': payout.travel.user.to_dict() if payout.travel.user else None
            }

        db.close()

        return render_template(
            'pages/financial/accountability.html',
            payout=payout_data
        )

    except Exception as e:
        print(f"Erro ao carregar prestação de contas: {e}")
        flash('Erro ao carregar prestação de contas', 'error')
        return redirect(url_for('admin.financial_payouts_list'))


def financial_payouts_list():
    """Lista todos os repasses financeiros do usuário logado"""
    try:
        db = SessionLocal()

        # Obter ID do usuário logado
        user_id = session.get('user_id')

        if not user_id:
            flash('Usuário não autenticado', 'error')
            return redirect(url_for('auth.login'))

        # Buscar todos os payouts do usuário logado com relacionamentos
        payouts = db.query(TravelPayout)\
            .filter_by(member_id=user_id)\
            .join(Travel)\
            .options(
                joinedload(TravelPayout.travel).joinedload(Travel.city).joinedload(City.state),
                joinedload(TravelPayout.travel).joinedload(Travel.user)
            )\
            .order_by(TravelPayout.created_at.desc())\
            .all()

        # Converter para dicionários
        payouts_data = []
        for payout in payouts:
            payout_dict = payout.to_dict()
            # Adicionar informações da viagem
            if payout.travel:
                payout_dict['travel_info'] = {
                    'id': payout.travel.id,
                    'purpose': payout.travel.purpose,
                    'departure_date': payout.travel.departure_date.isoformat() if payout.travel.departure_date else None,
                    'return_date': payout.travel.return_date.isoformat() if payout.travel.return_date else None,
                    'status': payout.travel.status.value if payout.travel.status else None,
                    'city': payout.travel.city.to_dict() if payout.travel.city else None,
                    'user': payout.travel.user.to_dict() if payout.travel.user else None
                }
            payouts_data.append(payout_dict)

        # Calcular totais
        total_pending = sum(p['amount'] for p in payouts_data if p['status'] == 'pending')
        total_paid = sum(p['amount'] for p in payouts_data if p['status'] == 'paid')
        total_all = sum(p['amount'] for p in payouts_data)

        db.close()

        return render_template(
            'pages/financial/list.html',
            payouts=payouts_data,
            total_payouts=len(payouts_data),
            total_pending=total_pending,
            total_paid=total_paid,
            total_all=total_all
        )

    except Exception as e:
        print(f"Erro ao listar repasses financeiros: {e}")
        flash('Erro ao carregar lista de repasses financeiros', 'error')
        return redirect(url_for('admin.dashboard'))
