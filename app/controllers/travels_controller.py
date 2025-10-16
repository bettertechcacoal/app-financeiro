# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app.models.database import SessionLocal
from app.models.travel import Travel, TravelStatus
from app.models.travel_passenger import TravelPassenger
from app.models.travel_payout import TravelPayout, PayoutStatus
from app.models.user import User
from app.models.city import City
from app.models.state import State
from app.models.vehicle import Vehicle
from app.models.vehicle_travel_history import VehicleTravelHistory
from datetime import datetime
from decimal import Decimal


def travels_list():
    """Lista todas as viagens do usuário logado"""
    try:
        db = SessionLocal()

        # Buscar todas as viagens ordenadas por data de criação (mais recentes primeiro)
        travels = db.query(Travel).order_by(Travel.created_at.desc()).all()

        # Converter para dicionários
        travels_data = [travel.to_dict() for travel in travels]

        db.close()

        return render_template(
            'pages/travels/list.html',
            travels=travels_data,
            total_travels=len(travels_data)
        )

    except Exception as e:
        print(f"Erro ao listar viagens: {e}")
        flash('Erro ao carregar lista de viagens', 'error')
        return redirect(url_for('admin.dashboard'))


def travels_create():
    """Exibe formulário de criação de viagem"""
    try:
        db = SessionLocal()

        # Buscar todas as cidades e usuários para os selects
        cities = db.query(City).join(State).order_by(State.name, City.name).all()
        users = db.query(User).filter_by(is_active=True).order_by(User.name).all()

        cities_data = [city.to_dict() for city in cities]
        users_data = [user.to_dict() for user in users]

        db.close()

        return render_template(
            'pages/travels/form.html',
            travel=None,
            cities=cities_data,
            users=users_data
        )

    except Exception as e:
        print(f"Erro ao carregar formulário: {e}")
        flash('Erro ao carregar formulário de viagem', 'error')
        return redirect(url_for('admin.travels_list'))


def travels_store():
    """Salva uma nova viagem"""
    try:
        db = SessionLocal()

        # Obter dados do formulário
        user_id = request.form.get('user_id')
        city_id = request.form.get('city_id')
        purpose = request.form.get('purpose')
        departure_date = request.form.get('departure_date')
        return_date = request.form.get('return_date')
        notes = request.form.get('notes')
        needs_vehicle = request.form.get('needs_vehicle') == '1'

        # Validações básicas
        if not all([user_id, city_id, purpose, departure_date, return_date]):
            flash('Preencha todos os campos obrigatórios', 'error')
            return redirect(url_for('admin.travels_create'))

        # Converter strings de data para datetime
        departure_datetime = datetime.fromisoformat(departure_date)
        return_datetime = datetime.fromisoformat(return_date)

        # Validar se data de retorno é posterior à data de saída
        if return_datetime <= departure_datetime:
            flash('A data de retorno deve ser posterior à data de saída', 'error')
            return redirect(url_for('admin.travels_create'))

        # Criar nova viagem
        new_travel = Travel(
            user_id=int(user_id),
            city_id=int(city_id),
            purpose=purpose,
            departure_date=departure_datetime,
            return_date=return_datetime,
            notes=notes,
            needs_vehicle=needs_vehicle,
            status=TravelStatus.PENDING
        )

        db.add(new_travel)
        db.flush()  # Para obter o ID da viagem

        # Processar passageiros
        passenger_ids = request.form.getlist('passengers[]')
        if passenger_ids:
            for passenger_id in passenger_ids:
                if passenger_id:  # Verificar se não está vazio
                    new_passenger = TravelPassenger(
                        travel_id=new_travel.id,
                        user_id=int(passenger_id)
                    )
                    db.add(new_passenger)

        db.commit()
        db.close()

        flash('Viagem cadastrada com sucesso!', 'success')
        return redirect(url_for('admin.travels_list'))

    except Exception as e:
        db.rollback()
        db.close()
        print(f"Erro ao criar viagem: {e}")
        flash('Erro ao cadastrar viagem', 'error')
        return redirect(url_for('admin.travels_create'))


def travels_edit(travel_id):
    """Exibe formulário de edição de viagem"""
    try:
        db = SessionLocal()

        # Buscar viagem
        travel = db.query(Travel).filter_by(id=travel_id).first()

        if not travel:
            flash('Viagem não encontrada', 'error')
            return redirect(url_for('admin.travels_list'))

        # Buscar cidades e usuários para os selects
        cities = db.query(City).join(State).order_by(State.name, City.name).all()
        users = db.query(User).filter_by(is_active=True).order_by(User.name).all()

        travel_data = travel.to_dict()
        cities_data = [city.to_dict() for city in cities]
        users_data = [user.to_dict() for user in users]

        db.close()

        return render_template(
            'pages/travels/form.html',
            travel=travel_data,
            cities=cities_data,
            users=users_data
        )

    except Exception as e:
        print(f"Erro ao carregar viagem: {e}")
        flash('Erro ao carregar dados da viagem', 'error')
        return redirect(url_for('admin.travels_list'))


def travels_update(travel_id):
    """Atualiza uma viagem existente"""
    try:
        db = SessionLocal()

        # Buscar viagem
        travel = db.query(Travel).filter_by(id=travel_id).first()

        if not travel:
            flash('Viagem não encontrada', 'error')
            return redirect(url_for('admin.travels_list'))

        # Obter dados do formulário
        user_id = request.form.get('user_id')
        city_id = request.form.get('city_id')
        purpose = request.form.get('purpose')
        departure_date = request.form.get('departure_date')
        return_date = request.form.get('return_date')
        notes = request.form.get('notes')
        needs_vehicle = request.form.get('needs_vehicle') == '1'
        status = request.form.get('status')

        # Validações básicas
        if not all([user_id, city_id, purpose, departure_date, return_date]):
            flash('Preencha todos os campos obrigatórios', 'error')
            return redirect(url_for('admin.travels_edit', travel_id=travel_id))

        # Converter strings de data para datetime
        departure_datetime = datetime.fromisoformat(departure_date)
        return_datetime = datetime.fromisoformat(return_date)

        # Validar se data de retorno é posterior à data de saída
        if return_datetime <= departure_datetime:
            flash('A data de retorno deve ser posterior à data de saída', 'error')
            return redirect(url_for('admin.travels_edit', travel_id=travel_id))

        # Atualizar viagem
        travel.user_id = int(user_id)
        travel.city_id = int(city_id)
        travel.purpose = purpose
        travel.departure_date = departure_datetime
        travel.return_date = return_datetime
        travel.notes = notes
        travel.needs_vehicle = needs_vehicle

        if status:
            travel.status = TravelStatus(status)

        # Processar passageiros
        passenger_ids = request.form.getlist('passengers[]')

        # Remover passageiros antigos
        db.query(TravelPassenger).filter_by(travel_id=travel_id).delete()

        # Adicionar novos passageiros
        if passenger_ids:
            for passenger_id in passenger_ids:
                if passenger_id:  # Verificar se não está vazio
                    new_passenger = TravelPassenger(
                        travel_id=travel_id,
                        user_id=int(passenger_id)
                    )
                    db.add(new_passenger)

        db.commit()
        db.close()

        flash('Viagem atualizada com sucesso!', 'success')
        return redirect(url_for('admin.travels_edit', travel_id=travel_id))

    except Exception as e:
        db.rollback()
        db.close()
        print(f"Erro ao atualizar viagem: {e}")
        flash('Erro ao atualizar viagem', 'error')
        return redirect(url_for('admin.travels_edit', travel_id=travel_id))


def travels_delete(travel_id):
    """Remove uma viagem"""
    try:
        db = SessionLocal()

        # Buscar viagem
        travel = db.query(Travel).filter_by(id=travel_id).first()

        if not travel:
            flash('Viagem não encontrada', 'error')
            return redirect(url_for('admin.travels_list'))

        db.delete(travel)
        db.commit()
        db.close()

        flash('Viagem removida com sucesso!', 'success')
        return redirect(url_for('admin.travels_list'))

    except Exception as e:
        db.rollback()
        db.close()
        print(f"Erro ao remover viagem: {e}")
        flash('Erro ao remover viagem', 'error')
        return redirect(url_for('admin.travels_list'))


def travels_cancel(travel_id):
    """Cancela uma viagem"""
    try:
        db = SessionLocal()

        # Buscar viagem
        travel = db.query(Travel).filter_by(id=travel_id).first()

        if not travel:
            flash('Viagem não encontrada', 'error')
            return redirect(url_for('admin.travels_list'))

        # Verificar se a viagem pode ser cancelada
        if travel.status == TravelStatus.COMPLETED:
            flash('Não é possível cancelar uma viagem já concluída', 'error')
            return redirect(url_for('admin.travels_list'))

        # Atualizar status para cancelada
        travel.status = TravelStatus.CANCELLED

        db.commit()
        db.close()

        flash('Viagem cancelada com sucesso!', 'success')
        return redirect(url_for('admin.travels_list'))

    except Exception as e:
        db.rollback()
        db.close()
        print(f"Erro ao cancelar viagem: {e}")
        flash('Erro ao cancelar viagem', 'error')
        return redirect(url_for('admin.travels_list'))


def travels_analyze(travel_id):
    """Exibe tela de análise de viagem (wizard)"""
    db = SessionLocal()

    # Buscar viagem
    travel = db.query(Travel).filter_by(id=travel_id).first()

    if not travel:
        flash('Viagem não encontrada', 'error')
        return redirect(url_for('admin.travels_list'))

    # Verificar se já foi aprovada/rejeitada
    if travel.status != TravelStatus.PENDING:
        flash('Esta viagem já foi analisada', 'warning')
        return redirect(url_for('admin.travels_list'))

    travel_data = travel.to_dict()

    # Calcular dias de viagem
    if travel.departure_date and travel.return_date:
        delta = travel.return_date.date() - travel.departure_date.date()
        travel_data['days'] = delta.days + 1
    else:
        travel_data['days'] = 0

    db.close()

    return render_template(
        'pages/travels/analyze.html',
        travel=travel_data
    )


def travels_analyze_process(travel_id):
    """Processa a análise da viagem"""
    try:
        db = SessionLocal()

        # Buscar viagem
        travel = db.query(Travel).filter_by(id=travel_id).first()

        if not travel:
            flash('Viagem não encontrada', 'error')
            return redirect(url_for('admin.travels_list'))

        # Verificar se já foi aprovada/rejeitada
        if travel.status != TravelStatus.PENDING:
            flash('Esta viagem já foi analisada', 'warning')
            return redirect(url_for('admin.travels_list'))

        # Obter dados do formulário
        action = request.form.get('action')  # 'approve' ou 'reject'
        vehicle_id = request.form.get('vehicle_id')
        admin_notes = request.form.get('admin_notes', '').strip()

        if action == 'approve':
            # Aprovar viagem
            travel.status = TravelStatus.APPROVED
            travel.approved_by = session.get('user_id')
            travel.approved_at = datetime.now()

            # Se solicitou veículo e foi selecionado um, criar registro no histórico
            if travel.needs_vehicle and vehicle_id:
                # Buscar a quilometragem atual do veículo
                vehicle = db.query(Vehicle).filter_by(id=int(vehicle_id)).first()
                if vehicle:
                    current_km = vehicle.get_current_km(db)

                    # Criar registro de alocação de veículo
                    vehicle_history = VehicleTravelHistory(
                        vehicle_id=int(vehicle_id),
                        travel_id=travel.id,
                        user_id=session.get('user_id'),
                        previous_km=current_km,
                        current_km=current_km,  # Será atualizado após a viagem
                        km_traveled=0  # Será calculado após a viagem
                    )
                    db.add(vehicle_history)

            # Processar repasses financeiros
            # Buscar todos os campos que começam com 'financial_amount_user_'
            for key in request.form.keys():
                if key.startswith('financial_amount_user_'):
                    member_id = int(key.replace('financial_amount_user_', ''))
                    amount_str = request.form.get(key, '0').strip()

                    if amount_str and amount_str != '0' and amount_str != '':
                        try:
                            amount = Decimal(amount_str)

                            if amount > 0:
                                # Criar registro de payout
                                payout = TravelPayout(
                                    travel_id=travel.id,
                                    member_id=member_id,
                                    amount=amount,
                                    status=PayoutStatus.PENDING
                                )
                                db.add(payout)
                        except (ValueError, TypeError):
                            # Ignorar valores inválidos
                            pass

            if admin_notes:
                travel.admin_notes = admin_notes

            db.commit()
            flash('Viagem aprovada com sucesso!', 'success')

        elif action == 'reject':
            # Rejeitar viagem
            travel.status = TravelStatus.CANCELLED

            if admin_notes:
                travel.admin_notes = f"[REJEITADA] {admin_notes}"
            else:
                travel.admin_notes = "[REJEITADA] Viagem não aprovada"

            db.commit()
            flash('Viagem rejeitada', 'info')

        else:
            flash('Ação inválida', 'error')

        db.close()
        return redirect(url_for('admin.travels_list'))

    except Exception as e:
        db.rollback()
        db.close()
        print(f"Erro ao processar análise: {e}")
        flash('Erro ao processar análise da viagem', 'error')
        return redirect(url_for('admin.travels_list'))


def travels_view(travel_id):
    """Exibe resumo completo da viagem"""
    try:
        db = SessionLocal()

        # Buscar viagem
        travel = db.query(Travel).filter_by(id=travel_id).first()

        if not travel:
            flash('Viagem não encontrada', 'error')
            return redirect(url_for('admin.travels_list'))

        travel_data = travel.to_dict()

        # Calcular dias de viagem
        if travel.departure_date and travel.return_date:
            delta = travel.return_date.date() - travel.departure_date.date()
            travel_data['days'] = delta.days + 1
        else:
            travel_data['days'] = 0

        db.close()

        return render_template(
            'pages/travels/view.html',
            travel=travel_data
        )

    except Exception as e:
        print(f"Erro ao carregar resumo da viagem: {e}")
        flash('Erro ao carregar dados da viagem', 'error')
        return redirect(url_for('admin.travels_list'))


def get_available_vehicles_api():
    """API para buscar veículos disponíveis"""
    try:
        db = SessionLocal()

        # Buscar veículos ativos
        vehicles = db.query(Vehicle).filter_by(is_active=True).order_by(Vehicle.brand, Vehicle.model).all()

        vehicles_data = [vehicle.to_dict() for vehicle in vehicles]
        db.close()

        return jsonify({'success': True, 'vehicles': vehicles_data})

    except Exception as e:
        print(f"Erro ao buscar veículos: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
