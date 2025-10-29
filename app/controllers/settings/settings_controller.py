# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app.models.parameter import Parameter, ParameterType
from app.models.parameter_group import ParameterGroup
from app.models.database import get_db
from sqlalchemy import desc
from collections import defaultdict


def settings_list():
    """Lista todos os parâmetros do sistema agrupados"""
    db = get_db()
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('auth.login'))

    # Buscar todos os grupos ordenados por ordem
    groups = db.query(ParameterGroup).order_by(ParameterGroup.order).all()

    # Buscar todos os parâmetros
    parameters = db.query(Parameter).order_by(Parameter.parameter).all()

    # Agrupar parâmetros por grupo
    grouped_parameters = defaultdict(list)
    for param in parameters:
        if param.group_id:
            grouped_parameters[param.group_id].append(param)
        else:
            grouped_parameters[None].append(param)

    return render_template(
        'pages/settings/list.html',
        groups=groups,
        grouped_parameters=grouped_parameters
    )


def settings_create():
    """Exibe formulário para criar novo parâmetro"""
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        db = get_db()

        try:
            # Validar se o parâmetro já existe
            existing = db.query(Parameter).filter_by(
                parameter=request.form.get('parameter')
            ).first()

            if existing:
                flash('Erro: Já existe um parâmetro com este nome!', 'error')
                return redirect(url_for('admin.settings_create'))

            # Criar novo parâmetro
            param_type = ParameterType[request.form.get('type').upper()]
            parameter = Parameter(
                parameter=request.form.get('parameter').upper().strip(),
                type=param_type,
                description=request.form.get('description'),
                value=request.form.get('value', ''),
                options=request.form.get('options') if param_type == ParameterType.SELECT else None
            )

            db.add(parameter)
            db.commit()

            flash('Parâmetro criado com sucesso!', 'success')
            return redirect(url_for('admin.settings_list'))

        except Exception as e:
            db.rollback()
            flash(f'Erro ao criar parâmetro: {str(e)}', 'error')
            return redirect(url_for('admin.settings_create'))

    return render_template('pages/settings/create.html')


def settings_update():
    """Atualiza múltiplos parâmetros de uma vez"""
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'success': False, 'message': 'Você precisa estar autenticado'}), 401

    try:
        db = get_db()
        data = request.get_json()
        parameters = data.get('parameters', [])

        updated_count = 0
        for param_data in parameters:
            param_id = param_data.get('id')
            param_value = param_data.get('value', '')

            parameter = db.query(Parameter).filter_by(id=param_id).first()
            if parameter:
                # Atualizar valor baseado no tipo
                if parameter.type == ParameterType.CHECKBOX:
                    parameter.value = 'S' if param_value == 'S' else 'N'
                else:
                    parameter.value = param_value
                updated_count += 1

        db.commit()

        return jsonify({
            'success': True,
            'message': 'Parâmetros salvos com sucesso!'
        })

    except Exception as e:
        db.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao atualizar parâmetros: {str(e)}'
        }), 500


def get_parameter_api(parameter_name):
    """API para buscar parâmetro por nome"""
    try:
        db = get_db()
        parameter = db.query(Parameter).filter_by(parameter=parameter_name.upper()).first()

        if parameter:
            return jsonify({
                'success': True,
                'value': parameter.value,
                'description': parameter.description
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Parâmetro não encontrado'
            }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def update_parameter_api(parameter_name):
    """API para atualizar parâmetro por nome"""
    try:
        db = get_db()
        parameter = db.query(Parameter).filter_by(parameter=parameter_name.upper()).first()

        if not parameter:
            # Criar parâmetro se não existir
            data = request.get_json()

            # Buscar grupo de Integrações para parâmetros do Movidesk
            group_id = None
            if 'MOVIDESK' in parameter_name.upper():
                integrations_group = db.query(ParameterGroup).filter_by(name='Integrações').first()
                if integrations_group:
                    group_id = integrations_group.id

            parameter = Parameter(
                parameter=parameter_name.upper(),
                type=ParameterType.TEXT,
                description=f'Configuração automática: {parameter_name}',
                value=data.get('value', ''),
                group_id=group_id
            )
            db.add(parameter)
        else:
            # Atualizar valor
            data = request.get_json()
            parameter.value = data.get('value', '')

        db.commit()

        # Se for parâmetro de sincronização do Movidesk, recarregar scheduler imediatamente
        if parameter_name.upper() == 'MOVIDESK_SYNC_SCHEDULES':
            from app.services.scheduler_service import load_sync_schedules
            load_sync_schedules()
            print("[SCHEDULER] Horários recarregados imediatamente após alteração")

        return jsonify({
            'success': True,
            'message': 'Parâmetro atualizado com sucesso'
        })

    except Exception as e:
        db.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
