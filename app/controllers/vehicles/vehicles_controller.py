# -*- coding: utf-8 -*-
"""
Controller: Vehicles
Gerencia veículos da frota
"""

from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app.models.database import SessionLocal
from app.models.vehicle import Vehicle
from app.models.maintenance_type import MaintenanceType
from app.models.vehicle_maintenance_config import VehicleMaintenanceConfig
from app.utils.permissions_helper import permission_required
from sqlalchemy import or_, desc
from datetime import datetime


@permission_required('veiculos_view')
def vehicles_list():
    """Lista todos os veículos cadastrados"""
    db = SessionLocal()
    try:
        # Filtros
        search = request.args.get('search', '')
        status = request.args.get('status', 'all')  # Alterado de 'active' para 'all'

        # Query base
        query = db.query(Vehicle)

        # Aplicar filtro de status
        if status == 'active':
            query = query.filter(Vehicle.is_active == True)
        elif status == 'inactive':
            query = query.filter(Vehicle.is_active == False)
        # Se status == 'all', não aplica filtro e mostra todos

        # Aplicar busca
        if search:
            query = query.filter(
                or_(
                    Vehicle.plate.ilike(f'%{search}%'),
                    Vehicle.model.ilike(f'%{search}%'),
                    Vehicle.brand.ilike(f'%{search}%')
                )
            )

        # Ordenar
        vehicles = query.order_by(desc(Vehicle.created_at)).all()

        return render_template(
            'pages/vehicles/list.html',
            vehicles=vehicles,
            search=search,
            status=status
        )

    finally:
        db.close()


@permission_required('veiculos_create')
def vehicles_create():
    """Cria um novo veículo"""
    db = SessionLocal()
    try:
        if request.method == 'GET':
            return render_template('pages/vehicles/form.html')

        # POST - Criar veículo
        plate = request.form.get('plate', '').strip().upper()
        model = request.form.get('model', '').strip()
        brand = request.form.get('brand', '').strip()
        year = request.form.get('year', type=int)

        # Validações
        if not plate or not model or not brand or not year:
            flash('Preencha todos os campos obrigatórios', 'error')
            return redirect(url_for('admin.vehicles_create'))

        # Verificar se placa já existe
        existing = db.query(Vehicle).filter(Vehicle.plate == plate).first()
        if existing:
            flash(f'Já existe um veículo cadastrado com a placa {plate}', 'error')
            return redirect(url_for('admin.vehicles_create'))

        # Criar veículo
        vehicle = Vehicle(
            plate=plate,
            model=model,
            brand=brand,
            year=year,
            is_active=True
        )

        db.add(vehicle)
        db.commit()

        flash(f'Veículo {plate} cadastrado com sucesso!', 'success')
        return redirect(url_for('admin.vehicles_list'))

    except Exception as e:
        db.rollback()
        flash(f'Erro ao cadastrar veículo: {str(e)}', 'error')
        return redirect(url_for('admin.vehicles_create'))
    finally:
        db.close()


@permission_required('veiculos_edit')
def vehicles_edit(vehicle_id):
    """Edita um veículo existente"""
    db = SessionLocal()
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            flash('Veículo não encontrado', 'error')
            return redirect(url_for('admin.vehicles_list'))

        if request.method == 'GET':
            # Carregar tipos de manutenção para o select
            maintenance_types = db.query(MaintenanceType).order_by(MaintenanceType.name).all()
            return render_template('pages/vehicles/form.html', vehicle=vehicle, maintenance_types=maintenance_types)

        # POST - Atualizar veículo
        vehicle.model = request.form.get('model', '').strip()
        vehicle.brand = request.form.get('brand', '').strip()
        vehicle.year = request.form.get('year', type=int)
        vehicle.is_active = request.form.get('is_active') == 'on'

        db.commit()

        flash(f'Veículo {vehicle.plate} atualizado com sucesso!', 'success')
        return redirect(url_for('admin.vehicles_list'))

    except Exception as e:
        db.rollback()
        flash(f'Erro ao atualizar veículo: {str(e)}', 'error')
        return redirect(url_for('admin.vehicles_list'))
    finally:
        db.close()


@permission_required('veiculos_view')
def vehicles_details(vehicle_id):
    """Exibe detalhes de um veículo"""
    db = SessionLocal()
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            flash('Veículo não encontrado', 'error')
            return redirect(url_for('admin.vehicles_list'))

        # Temporariamente comentado até as tabelas serem criadas
        pending_issues = []
        upcoming_maintenance = []
        overdue_maintenance = []

        return render_template(
            'pages/vehicles/details.html',
            vehicle=vehicle,
            pending_issues=pending_issues,
            upcoming_maintenance=upcoming_maintenance,
            overdue_maintenance=overdue_maintenance
        )

    except Exception as e:
        flash(f'Erro ao carregar detalhes: {str(e)}', 'error')
        return redirect(url_for('admin.vehicles_list'))
    finally:
        db.close()


@permission_required('veiculos_delete')
def vehicles_toggle_status(vehicle_id):
    """Alterna o status ativo/inativo de um veículo"""
    db = SessionLocal()
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            flash('Veículo não encontrado', 'error')
            return redirect(url_for('admin.vehicles_list'))

        # Alternar status
        vehicle.is_active = not vehicle.is_active
        db.commit()

        status_text = 'ativado' if vehicle.is_active else 'inativado'
        flash(f'Veículo {vehicle.plate} {status_text} com sucesso!', 'success')
        return redirect(url_for('admin.vehicles_list'))

    except Exception as e:
        db.rollback()
        flash(f'Erro ao alterar status do veículo: {str(e)}', 'error')
        return redirect(url_for('admin.vehicles_list'))
    finally:
        db.close()


# ========== API: Configurações de Manutenção ==========

@permission_required('veiculos_edit')
def vehicles_add_maintenance_config(vehicle_id):
    """API: Adiciona uma configuração de manutenção ao veículo"""
    db = SessionLocal()
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            return jsonify({'success': False, 'message': 'Veículo não encontrado'}), 404

        data = request.get_json()
        maintenance_type_id = data.get('maintenance_type_id')
        km_interval = data.get('km_interval')

        # Validações
        if not maintenance_type_id or not km_interval:
            return jsonify({'success': False, 'message': 'Dados incompletos'}), 400

        # Verificar se já existe configuração para este tipo
        existing = db.query(VehicleMaintenanceConfig).filter(
            VehicleMaintenanceConfig.vehicle_id == vehicle_id,
            VehicleMaintenanceConfig.maintenance_type_id == maintenance_type_id
        ).first()

        if existing:
            return jsonify({'success': False, 'message': 'Já existe uma configuração para este tipo de manutenção'}), 400

        # Criar configuração
        config = VehicleMaintenanceConfig(
            vehicle_id=vehicle_id,
            maintenance_type_id=maintenance_type_id,
            km_interval=km_interval,
            is_active=True
        )

        db.add(config)
        db.commit()

        return jsonify({
            'success': True,
            'message': 'Configuração adicionada com sucesso!',
            'config': config.to_dict()
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': f'Erro ao adicionar configuração: {str(e)}'}), 500
    finally:
        db.close()


@permission_required('veiculos_edit')
def vehicles_remove_maintenance_config(vehicle_id, config_id):
    """API: Remove uma configuração de manutenção"""
    db = SessionLocal()
    try:
        config = db.query(VehicleMaintenanceConfig).filter(
            VehicleMaintenanceConfig.id == config_id,
            VehicleMaintenanceConfig.vehicle_id == vehicle_id
        ).first()

        if not config:
            return jsonify({'success': False, 'message': 'Configuração não encontrada'}), 404

        db.delete(config)
        db.commit()

        return jsonify({'success': True, 'message': 'Configuração removida com sucesso!'}), 200

    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': f'Erro ao remover configuração: {str(e)}'}), 500
    finally:
        db.close()
