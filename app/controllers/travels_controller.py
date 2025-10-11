# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, session
from app.models.database import SessionLocal
from app.models.travel import Travel, TravelStatus
from app.models.user import User
from app.models.city import City
from app.models.state import State
from datetime import datetime


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
        description = request.form.get('description')
        departure_date = request.form.get('departure_date')
        return_date = request.form.get('return_date')
        notes = request.form.get('notes')

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
            description=description,
            departure_date=departure_datetime,
            return_date=return_datetime,
            notes=notes,
            status=TravelStatus.PENDING
        )

        db.add(new_travel)
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
        description = request.form.get('description')
        departure_date = request.form.get('departure_date')
        return_date = request.form.get('return_date')
        notes = request.form.get('notes')
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
        travel.description = description
        travel.departure_date = departure_datetime
        travel.return_date = return_datetime
        travel.notes = notes

        if status:
            travel.status = TravelStatus(status)

        db.commit()
        db.close()

        flash('Viagem atualizada com sucesso!', 'success')
        return redirect(url_for('admin.travels_list'))

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


def travels_approve(travel_id):
    """Aprova uma viagem"""
    try:
        db = SessionLocal()

        # Buscar viagem
        travel = db.query(Travel).filter_by(id=travel_id).first()

        if not travel:
            flash('Viagem não encontrada', 'error')
            return redirect(url_for('admin.travels_list'))

        # Atualizar status
        travel.status = TravelStatus.APPROVED
        travel.approved_at = datetime.now()
        # TODO: Implementar approved_by quando houver autenticação completa
        # travel.approved_by = session.get('user_id')

        db.commit()
        db.close()

        flash('Viagem aprovada com sucesso!', 'success')
        return redirect(url_for('admin.travels_list'))

    except Exception as e:
        db.rollback()
        db.close()
        print(f"Erro ao aprovar viagem: {e}")
        flash('Erro ao aprovar viagem', 'error')
        return redirect(url_for('admin.travels_list'))
