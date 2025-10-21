# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app.models.database import SessionLocal
from app.models.travel_payout import TravelPayout
from app.models.travel_statement import TravelStatement, StatementStatus
from app.models.travel import Travel
from app.models.user import User
from app.models.city import City
from app.models.state import State
from sqlalchemy.orm import joinedload
from sqlalchemy import case, func
import json


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
        from app.models.vehicle_travel_history import VehicleTravelHistory
        from app.models.vehicle import Vehicle

        payout = db.query(TravelPayout)\
            .filter_by(id=payout_id, member_id=user_id)\
            .join(Travel)\
            .options(
                joinedload(TravelPayout.travel).joinedload(Travel.city).joinedload(City.state),
                joinedload(TravelPayout.travel).joinedload(Travel.driver_user),
                joinedload(TravelPayout.travel).joinedload(Travel.vehicle_history).joinedload(VehicleTravelHistory.vehicle)
            )\
            .first()

        if not payout:
            flash('Repasse não encontrado ou você não tem permissão para acessá-lo', 'error')
            return redirect(url_for('admin.financial_payouts_list'))

        payout_data = payout.to_dict()

        # Buscar prestação de contas existente (se houver)
        existing_statement = db.query(TravelStatement).filter_by(payout_id=payout_id).first()
        if existing_statement:
            payout_data['existing_statement'] = existing_statement.to_dict()
        else:
            payout_data['existing_statement'] = None

        # Adicionar informações da viagem
        if payout.travel:
            # Pegar o veículo alocado (se houver) do histórico
            allocated_vehicle = None
            if payout.travel.vehicle_history:
                # Pegar o último registro de veículo para esta viagem
                last_vehicle_history = payout.travel.vehicle_history[-1] if payout.travel.vehicle_history else None
                if last_vehicle_history and last_vehicle_history.vehicle:
                    allocated_vehicle = last_vehicle_history.vehicle.to_dict()

            payout_data['travel_info'] = {
                'id': payout.travel.id,
                'purpose': payout.travel.purpose,
                'departure_date': payout.travel.departure_date.isoformat() if payout.travel.departure_date else None,
                'return_date': payout.travel.return_date.isoformat() if payout.travel.return_date else None,
                'status': payout.travel.status.value if payout.travel.status else None,
                'city': payout.travel.city.to_dict() if payout.travel.city else None,
                'driver_user': payout.travel.driver_user.to_dict() if payout.travel.driver_user else None,
                'vehicle': allocated_vehicle
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
        # Fazer LEFT JOIN com travel_statements para pegar o status da prestação de contas
        from sqlalchemy.orm import outerjoin

        payouts = db.query(TravelPayout, TravelStatement.status)\
            .outerjoin(TravelStatement, TravelPayout.id == TravelStatement.payout_id)\
            .filter(TravelPayout.member_id == user_id)\
            .join(Travel, TravelPayout.travel_id == Travel.id)\
            .options(
                joinedload(TravelPayout.travel).joinedload(Travel.city).joinedload(City.state),
                joinedload(TravelPayout.travel).joinedload(Travel.driver_user)
            )\
            .order_by(TravelPayout.created_at.desc())\
            .all()

        # Converter para dicionários
        payouts_data = []
        for payout, statement_status in payouts:
            payout_dict = payout.to_dict()

            # Substituir o status do payout pelo status da prestação de contas
            # Se não houver prestação de contas, usar 'draft' como padrão (pendente)
            if statement_status:
                payout_dict['accountability_status'] = statement_status.value
            else:
                payout_dict['accountability_status'] = 'draft'  # Pendente por padrão

            # Adicionar informações da viagem
            if payout.travel:
                payout_dict['travel_info'] = {
                    'id': payout.travel.id,
                    'purpose': payout.travel.purpose,
                    'departure_date': payout.travel.departure_date.isoformat() if payout.travel.departure_date else None,
                    'return_date': payout.travel.return_date.isoformat() if payout.travel.return_date else None,
                    'status': payout.travel.status.value if payout.travel.status else None,
                    'city': payout.travel.city.to_dict() if payout.travel.city else None,
                    'driver_user': payout.travel.driver_user.to_dict() if payout.travel.driver_user else None
                }
            payouts_data.append(payout_dict)

        # Calcular totais
        total_all = sum(p['amount'] for p in payouts_data)

        db.close()

        return render_template(
            'pages/financial/list.html',
            payouts=payouts_data,
            total_payouts=len(payouts_data),
            total_all=total_all
        )

    except Exception as e:
        print(f"Erro ao listar repasses financeiros: {e}")
        flash('Erro ao carregar lista de repasses financeiros', 'error')
        return redirect(url_for('admin.dashboard'))


def financial_review_accountability(payout_id):
    """Exibe tela de análise/revisão da prestação de contas"""
    db = SessionLocal()

    # Obter ID do usuário logado
    user_id = session.get('user_id')

    if not user_id:
        flash('Usuário não autenticado', 'error')
        return redirect(url_for('auth.login'))

    # Buscar o payout do usuário logado
    from app.models.vehicle_travel_history import VehicleTravelHistory
    from app.models.vehicle import Vehicle

    payout = db.query(TravelPayout)\
        .filter_by(id=payout_id, member_id=user_id)\
        .join(Travel)\
        .options(
            joinedload(TravelPayout.travel).joinedload(Travel.city).joinedload(City.state),
            joinedload(TravelPayout.travel).joinedload(Travel.driver_user),
            joinedload(TravelPayout.travel).joinedload(Travel.vehicle_history).joinedload(VehicleTravelHistory.vehicle)
        )\
        .first()

    if not payout:
        db.close()
        flash('Repasse não encontrado ou você não tem permissão para acessá-lo', 'error')
        return redirect(url_for('admin.financial_payouts_list'))

    # Buscar prestação de contas
    statement = db.query(TravelStatement).filter_by(payout_id=payout_id).first()

    if not statement:
        db.close()
        flash('Prestação de contas não encontrada', 'warning')
        return redirect(url_for('admin.financial_payouts_list'))

    payout_data = payout.to_dict()
    payout_data['statement'] = statement.to_dict()

    # Adicionar informações da viagem
    if payout.travel:
        # Pegar o veículo alocado (se houver) do histórico
        allocated_vehicle = None
        if payout.travel.vehicle_history:
            last_vehicle_history = payout.travel.vehicle_history[-1] if payout.travel.vehicle_history else None
            if last_vehicle_history and last_vehicle_history.vehicle:
                allocated_vehicle = last_vehicle_history.vehicle.to_dict()

        payout_data['travel_info'] = {
            'id': payout.travel.id,
            'purpose': payout.travel.purpose,
            'departure_date': payout.travel.departure_date.isoformat() if payout.travel.departure_date else None,
            'return_date': payout.travel.return_date.isoformat() if payout.travel.return_date else None,
            'status': payout.travel.status.value if payout.travel.status else None,
            'city': payout.travel.city.to_dict() if payout.travel.city else None,
            'driver_user': payout.travel.driver_user.to_dict() if payout.travel.driver_user else None,
            'vehicle': allocated_vehicle
        }

    db.close()

    return render_template(
        'pages/financial/review.html',
        payout=payout_data
    )


def save_accountability(payout_id):
    """Salva ou atualiza a prestação de contas"""
    try:
        db = SessionLocal()
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({'success': False, 'error': 'Usuário não autenticado'}), 401

        # Verificar se o payout pertence ao usuário
        payout = db.query(TravelPayout).filter_by(id=payout_id, member_id=user_id).first()

        if not payout:
            db.close()
            return jsonify({'success': False, 'error': 'Repasse não encontrado'}), 404

        # Obter dados JSON do request
        data = request.get_json()
        statement_content = data.get('statement_content', {})
        status = data.get('status', 'draft')  # Status padrão é 'draft'

        # Validar status e converter para enum
        status_map = {
            'draft': StatementStatus.DRAFT,
            'submitted': StatementStatus.SUBMITTED,
            'returned': StatementStatus.RETURNED,
            'approved': StatementStatus.APPROVED
        }

        if status not in status_map:
            db.close()
            return jsonify({'success': False, 'error': 'Status inválido'}), 400

        status_enum = status_map[status]

        # Buscar ou criar prestação de contas
        statement = db.query(TravelStatement).filter_by(payout_id=payout_id).first()

        if statement:
            # Atualizar existente
            statement.statement_content = statement_content
            statement.status = status_enum
        else:
            # Criar nova
            statement = TravelStatement(
                payout_id=payout_id,
                statement_content=statement_content,
                status=status_enum
            )
            db.add(statement)

        db.commit()

        # Mensagem de sucesso baseada no status
        messages = {
            'draft': 'Rascunho salvo com sucesso!',
            'submitted': 'Prestação de contas enviada com sucesso!',
            'returned': 'Prestação de contas retornada para revisão',
            'approved': 'Prestação de contas aprovada!'
        }

        statement_id = statement.id
        db.close()

        return jsonify({
            'success': True,
            'message': messages.get(status, 'Prestação de contas salva com sucesso!'),
            'statement_id': statement_id
        })

    except Exception as e:
        if db:
            db.rollback()
            db.close()
        print(f"Erro ao salvar prestação de contas: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
