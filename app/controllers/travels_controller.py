# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app.models.database import SessionLocal
from app.models.travel import Travel, TravelStatus
from app.models.travel_passenger import TravelPassenger
from app.models.travel_payout import TravelPayout
from app.models.user import User
from app.models.city import City
from app.models.state import State
from app.models.vehicle import Vehicle
from app.models.vehicle_travel_history import VehicleTravelHistory
from app.utils.permissions_helper import permission_required
from datetime import datetime
from decimal import Decimal
from sqlalchemy import case, or_, and_
import sqlalchemy


def travels_list():
    """Lista viagens do usuário ou todas se tiver permissão"""
    try:
        db = SessionLocal()
        user_id = session.get('user_id')

        if not user_id:
            flash('Usuário não autenticado', 'error')
            return redirect(url_for('auth.login'))

        from app.utils.permissions_helper import user_has_permission
        can_approve_travels = user_has_permission('travels_approve')
        can_view_all_travels = user_has_permission('travels_view_all')

        status_label = case(
            (Travel.status == TravelStatus.PENDING, 'Aguardando aprovação'),
            (Travel.status == TravelStatus.APPROVED, 'Aprovada'),
            (Travel.status == TravelStatus.IN_PROGRESS, 'Em andamento'),
            (Travel.status == TravelStatus.COMPLETED, 'Concluída'),
            (Travel.status == TravelStatus.CANCELLED, 'Cancelada'),
            else_='Desconhecido'
        ).label('status_label')

        from sqlalchemy import or_
        from sqlalchemy.orm import outerjoin

        if can_approve_travels or can_view_all_travels:
            results = db.query(Travel, status_label)\
                .order_by(Travel.created_at.desc())\
                .all()
        else:
            results = db.query(Travel, status_label)\
                .outerjoin(TravelPassenger, Travel.id == TravelPassenger.travel_id)\
                .filter(
                    or_(
                        Travel.driver_user_id == user_id,
                        TravelPassenger.user_id == user_id
                    )
                )\
                .distinct()\
                .order_by(Travel.created_at.desc())\
                .all()

        travels_data = []
        for travel, status_text in results:
            travel_dict = travel.to_dict()
            travel_dict['status_label'] = status_text
            travels_data.append(travel_dict)

        db.close()

        return render_template(
            'pages/travels/list.html',
            travels=travels_data,
            total_travels=len(travels_data),
            current_user_id=user_id
        )

    except Exception as e:
        print(f"Erro ao listar viagens: {e}")
        flash('Erro ao carregar lista de viagens', 'error')
        return redirect(url_for('admin.dashboard'))


def travels_create():
    """Exibe formulário de criação de viagem"""
    try:
        db = SessionLocal()

        # Buscar cidades
        cities = db.query(City).join(State).order_by(State.name, City.name).all()
        cities_data = [city.to_dict() for city in cities]

        # Verificar se usuário tem permissão para aprovar viagens
        from app.utils.permissions_helper import user_has_permission
        can_approve_travels = user_has_permission('travels_approve')
        can_create_retroactive = user_has_permission('travels_create_retroactive')

        # Buscar dados do usuário logado
        logged_user_id = session.get('user_id')
        logged_user = db.query(User).filter_by(id=logged_user_id).first()
        logged_user_data = logged_user.to_dict() if logged_user else None

        # Se tem permissão, busca todos os usuários; senão, apenas o próprio
        if can_approve_travels:
            users = db.query(User).filter_by(active=True).order_by(User.name).all()
        else:
            users = [logged_user] if logged_user else []

        users_data = [user.to_dict() for user in users]

        db.close()

        return render_template(
            'pages/travels/form.html',
            travel=None,
            cities=cities_data,
            users=users_data,
            can_approve_travels=can_approve_travels,
            can_create_retroactive=can_create_retroactive,
            logged_user=logged_user_data,
            can_edit=True  # Sempre pode editar ao criar
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

        # Validar data retroativa (apenas se não tiver permissão)
        from app.utils.permissions_helper import user_has_permission
        if departure_datetime.date() < datetime.now().date():
            if not user_has_permission('travels_create_retroactive'):
                flash('Você não tem permissão para lançar viagens com datas retroativas', 'error')
                return redirect(url_for('admin.travels_create'))

        # Criar nova viagem
        new_travel = Travel(
            driver_user_id=int(user_id),
            record_user_id=session.get('user_id'),
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

        # Enviar notificações sobre nova viagem
        try:
            from app.utils.notification_helper import send_notification
            from app.models.notification import NotificationType
            from app.models.user import User

            # Coletar IDs únicos de usuários que devem receber notificação
            notify_user_ids = set()

            # 1. Adicionar solicitante (driver)
            notify_user_ids.add(new_travel.driver_user_id)

            # 2. Adicionar passageiros
            if passenger_ids:
                for passenger_id in passenger_ids:
                    if passenger_id:
                        notify_user_ids.add(int(passenger_id))

            # 3. Adicionar usuários com permissão de aprovar viagens
            users_with_approve_permission = db.query(User).filter_by(active=True).all()
            for user in users_with_approve_permission:
                if user.has_permission('travels_approve'):
                    notify_user_ids.add(user.id)

            # Enviar notificação para cada usuário
            for user_id in notify_user_ids:
                send_notification(
                    user_id=user_id,
                    title='Nova Viagem Cadastrada',
                    message=f'Uma nova viagem para {new_travel.city.name} foi cadastrada e aguarda aprovação.',
                    notification_type=NotificationType.TRAVEL,
                    action_url=f'/admin/travels/{new_travel.id}/view',
                    action_text='Ver Viagem'
                )
        except Exception as e:
            # Falha silenciosa - viagem já foi criada
            print(f"Erro ao enviar notificações: {e}")

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

        # Verificar se a viagem está pendente
        if travel.status != TravelStatus.PENDING:
            flash('Apenas viagens pendentes podem ser editadas', 'error')
            return redirect(url_for('admin.travels_list'))

        # Buscar cidades
        cities = db.query(City).join(State).order_by(State.name, City.name).all()
        cities_data = [city.to_dict() for city in cities]

        travel_data = travel.to_dict()

        # Verificar se usuário tem permissão para aprovar viagens
        from app.utils.permissions_helper import user_has_permission
        can_approve_travels = user_has_permission('travels_approve')
        can_create_retroactive = user_has_permission('travels_create_retroactive')

        # Buscar dados do usuário logado
        logged_user_id = session.get('user_id')
        logged_user = db.query(User).filter_by(id=logged_user_id).first()
        logged_user_data = logged_user.to_dict() if logged_user else None

        # Verificar se o usuário pode editar (é o solicitante ou criador do registro)
        can_edit = (travel.driver_user_id == logged_user_id or travel.record_user_id == logged_user_id)

        # Se tem permissão, busca todos os usuários
        # Se não tem permissão, busca apenas o solicitante original da viagem (para manter no select)
        if can_approve_travels:
            users = db.query(User).filter_by(active=True).order_by(User.name).all()
        else:
            # Buscar o usuário que é o solicitante da viagem (driver_user)
            driver_user = db.query(User).filter_by(id=travel.driver_user_id).first()
            users = [driver_user] if driver_user else []

        users_data = [user.to_dict() for user in users]

        db.close()

        return render_template(
            'pages/travels/form.html',
            travel=travel_data,
            cities=cities_data,
            users=users_data,
            can_approve_travels=can_approve_travels,
            can_create_retroactive=can_create_retroactive,
            logged_user=logged_user_data,
            can_edit=can_edit
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

        # Verificar se a viagem está pendente
        if travel.status != TravelStatus.PENDING:
            flash('Apenas viagens pendentes podem ser editadas', 'error')
            return redirect(url_for('admin.travels_list'))

        # Verificar se o usuário pode editar (é o solicitante ou criador do registro)
        logged_user_id = session.get('user_id')
        can_edit = (travel.driver_user_id == logged_user_id or travel.record_user_id == logged_user_id)

        if not can_edit:
            flash('Você não tem permissão para editar esta viagem', 'error')
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

        # Validar data retroativa (apenas se não tiver permissão)
        from app.utils.permissions_helper import user_has_permission
        if departure_datetime.date() < datetime.now().date():
            if not user_has_permission('travels_create_retroactive'):
                flash('Você não tem permissão para lançar viagens com datas retroativas', 'error')
                return redirect(url_for('admin.travels_edit', travel_id=travel_id))

        # Atualizar viagem
        travel.driver_user_id = int(user_id)
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

        # Verificar se o usuário pode cancelar (apenas motorista ou quem registrou)
        current_user_id = session.get('user_id')
        if travel.driver_user_id != current_user_id and travel.record_user_id != current_user_id:
            flash('Você não tem permissão para cancelar esta viagem', 'error')
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


@permission_required('travels_approve')
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


@permission_required('travels_approve')
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

                    if amount_str and amount_str != '':
                        try:
                            amount = Decimal(amount_str)

                            if amount >= 0:
                                # Criar registro de payout (mesmo com valor 0 para prestação de contas)
                                payout = TravelPayout(
                                    travel_id=travel.id,
                                    member_id=member_id,
                                    amount=amount
                                )
                                db.add(payout)
                        except (ValueError, TypeError):
                            # Ignorar valores inválidos
                            pass

            if admin_notes:
                travel.admin_notes = admin_notes

            db.commit()
            flash('Viagem aprovada com sucesso!', 'success')

            # Enviar notificações sobre aprovação da viagem
            try:
                from app.utils.notification_helper import send_notification
                from app.models.notification import NotificationType

                notify_user_ids = set()

                # Adicionar solicitante (driver)
                notify_user_ids.add(travel.driver_user_id)

                # Adicionar passageiros
                passengers = db.query(TravelPassenger).filter_by(travel_id=travel.id).all()
                for passenger in passengers:
                    notify_user_ids.add(passenger.user_id)

                # Enviar notificação para cada usuário
                for user_id in notify_user_ids:
                    send_notification(
                        user_id=user_id,
                        title='Viagem Aprovada',
                        message=f'Sua viagem para {travel.city.name} foi aprovada!',
                        notification_type=NotificationType.TRAVEL,
                        action_url=f'/admin/travels/{travel.id}/view',
                        action_text='Ver Viagem'
                    )
            except Exception as e:
                print(f"Erro ao enviar notificações: {e}")

        elif action == 'reject':
            # Rejeitar viagem
            travel.status = TravelStatus.CANCELLED

            if admin_notes:
                travel.admin_notes = f"[REJEITADA] {admin_notes}"
            else:
                travel.admin_notes = "[REJEITADA] Viagem não aprovada"

            db.commit()
            flash('Viagem rejeitada', 'info')

            # Enviar notificações sobre rejeição da viagem
            try:
                from app.utils.notification_helper import send_notification
                from app.models.notification import NotificationType

                notify_user_ids = set()

                # Adicionar solicitante (driver)
                notify_user_ids.add(travel.driver_user_id)

                # Adicionar passageiros
                passengers = db.query(TravelPassenger).filter_by(travel_id=travel.id).all()
                for passenger in passengers:
                    notify_user_ids.add(passenger.user_id)

                # Enviar notificação para cada usuário
                for user_id in notify_user_ids:
                    send_notification(
                        user_id=user_id,
                        title='Viagem Rejeitada',
                        message=f'Sua viagem para {travel.city.name} foi rejeitada.',
                        notification_type=NotificationType.TRAVEL,
                        action_url=f'/admin/travels/{travel.id}/view',
                        action_text='Ver Viagem'
                    )
            except Exception as e:
                print(f"Erro ao enviar notificações: {e}")

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


def travels_check_conflicts():
    """API para verificar conflitos de viagens aprovadas ou pendentes"""
    try:
        data = request.get_json()
        driver_user_id = data.get('driver_user_id')
        passenger_ids = data.get('passenger_ids', [])
        departure_date = data.get('departure_date')
        return_date = data.get('return_date')
        current_travel_id = data.get('travel_id')

        if not all([driver_user_id, departure_date, return_date]):
            return jsonify({'success': False, 'error': 'Dados incompletos'}), 400

        db = SessionLocal()
        departure_dt = datetime.fromisoformat(departure_date)
        return_dt = datetime.fromisoformat(return_date)
        all_participant_ids = [int(driver_user_id)] + [int(pid) for pid in passenger_ids if pid]
        conflicts = []

        for user_id in all_participant_ids:
            conflicting_travels = db.query(Travel)\
                .outerjoin(TravelPassenger, Travel.id == TravelPassenger.travel_id)\
                .filter(
                    Travel.status.in_([TravelStatus.APPROVED, TravelStatus.PENDING]),
                    sqlalchemy.or_(
                        Travel.driver_user_id == user_id,
                        TravelPassenger.user_id == user_id
                    ),
                    sqlalchemy.or_(
                        sqlalchemy.and_(
                            Travel.departure_date <= departure_dt,
                            Travel.return_date >= departure_dt
                        ),
                        sqlalchemy.and_(
                            Travel.departure_date <= return_dt,
                            Travel.return_date >= return_dt
                        ),
                        sqlalchemy.and_(
                            Travel.departure_date >= departure_dt,
                            Travel.return_date <= return_dt
                        )
                    )
                )\
                .distinct()

            if current_travel_id:
                conflicting_travels = conflicting_travels.filter(Travel.id != current_travel_id)

            conflicting_travels = conflicting_travels.all()

            if conflicting_travels:
                user = db.query(User).filter_by(id=user_id).first()
                for travel in conflicting_travels:
                    conflicts.append({
                        'user_name': user.name if user else 'Usuário desconhecido',
                        'user_id': user_id,
                        'city': travel.city.name if travel.city else 'Cidade não informada',
                        'state': travel.city.state.uf if travel.city and travel.city.state else '',
                        'departure_date': travel.departure_date.strftime('%d/%m/%Y %H:%M'),
                        'return_date': travel.return_date.strftime('%d/%m/%Y %H:%M')
                    })

        db.close()

        if conflicts:
            return jsonify({'success': True, 'has_conflicts': True, 'conflicts': conflicts}), 200
        else:
            return jsonify({'success': True, 'has_conflicts': False, 'conflicts': []}), 200

    except Exception as e:
        print(f"Erro ao verificar conflitos: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


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
    """API para buscar veículos disponíveis e verificar conflitos de reserva"""
    try:
        db = SessionLocal()
        departure_date_str = request.args.get('departure_date')
        return_date_str = request.args.get('return_date')
        current_travel_id = request.args.get('travel_id')

        vehicles = db.query(Vehicle).filter_by(is_active=True).order_by(Vehicle.brand, Vehicle.model).all()
        vehicles_data = []

        for vehicle in vehicles:
            vehicle_dict = vehicle.to_dict()
            vehicle_dict['reserved'] = False

            if departure_date_str and return_date_str:
                try:
                    departure_dt = datetime.fromisoformat(departure_date_str.replace('Z', '+00:00'))
                    return_dt = datetime.fromisoformat(return_date_str.replace('Z', '+00:00'))

                    if departure_dt.tzinfo is not None:
                        departure_dt = departure_dt.replace(tzinfo=None)
                    if return_dt.tzinfo is not None:
                        return_dt = return_dt.replace(tzinfo=None)

                    from app.models.vehicle_travel_history import VehicleTravelHistory

                    conflicting_travels = db.query(Travel)\
                        .join(VehicleTravelHistory, Travel.id == VehicleTravelHistory.travel_id)\
                        .filter(
                            VehicleTravelHistory.vehicle_id == vehicle.id,
                            Travel.status == TravelStatus.APPROVED,
                            sqlalchemy.or_(
                                sqlalchemy.and_(
                                    Travel.departure_date <= departure_dt,
                                    Travel.return_date >= departure_dt
                                ),
                                sqlalchemy.and_(
                                    Travel.departure_date <= return_dt,
                                    Travel.return_date >= return_dt
                                ),
                                sqlalchemy.and_(
                                    Travel.departure_date >= departure_dt,
                                    Travel.return_date <= return_dt
                                )
                            )
                        )

                    if current_travel_id:
                        conflicting_travels = conflicting_travels.filter(Travel.id != int(current_travel_id))

                    if conflicting_travels.first():
                        vehicle_dict['reserved'] = True
                except:
                    pass

            vehicles_data.append(vehicle_dict)

        db.close()
        return jsonify({'success': True, 'vehicles': vehicles_data})

    except Exception as e:
        print(f"Erro ao buscar veículos: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
