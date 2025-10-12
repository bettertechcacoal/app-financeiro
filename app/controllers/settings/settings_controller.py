# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, session
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


def settings_update(parameter_id):
    """Atualiza o valor de um parâmetro inline"""
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('auth.login'))

    db = get_db()
    parameter = db.query(Parameter).filter_by(id=parameter_id).first()

    if not parameter:
        flash('Parâmetro não encontrado!', 'error')
        return redirect(url_for('admin.settings_list'))

    try:
        # Atualizar valor baseado no tipo
        if parameter.type == ParameterType.CHECKBOX:
            # Para checkbox, se estiver marcado vem 'S', senão vem vazio
            parameter.value = 'S' if request.form.get('value') == 'S' else 'N'
        else:
            parameter.value = request.form.get('value', '')

        db.commit()
        flash('Parâmetro atualizado com sucesso!', 'success')

    except Exception as e:
        db.rollback()
        flash(f'Erro ao atualizar parâmetro: {str(e)}', 'error')

    return redirect(url_for('admin.settings_list'))
