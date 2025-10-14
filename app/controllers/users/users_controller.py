# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, jsonify
from app.services.user_service import user_service
from app.services.group_service import group_service


def users_list():
    """Lista de usuários"""
    users = user_service.get_all_users()
    return render_template('pages/users/manage.html', users=users)


def user_new():
    """Formulário de novo usuário"""
    groups = group_service.get_all_groups()
    return render_template('pages/users/form.html', user=None, groups=groups, is_admin_edit=True, is_new=True)


def user_create():
    """Cria um novo usuário"""
    try:
        # Validação dos campos obrigatórios
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()

        errors = []

        if not name:
            errors.append('O campo "Nome" é obrigatório')

        if not email:
            errors.append('O campo "E-mail" é obrigatório')

        # Se houver erros de validação, retornar ao formulário com mensagens
        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('admin.user_new'))

        user_data = {
            'name': name,
            'email': email,
            'phone': request.form.get('phone'),
            'avatar': request.form.get('avatar'),
            'is_active': request.form.get('is_active', 'on') == 'on'
        }

        user = user_service.create_user(user_data)
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('admin.users_list'))
    except Exception as e:
        flash(f'Erro ao cadastrar usuário: {str(e)}', 'error')
        return redirect(url_for('admin.user_new'))


def user_edit(user_id):
    """Exibe formulário de edição de usuário"""
    user = user_service.get_user_with_groups(user_id)
    if not user:
        flash('Usuário não encontrado', 'error')
        return redirect(url_for('admin.users_list'))

    groups = group_service.get_all_groups()
    return render_template('pages/users/form.html', user=user, groups=groups, is_admin_edit=True, is_new=False)


def user_update(user_id):
    """Atualiza um usuário"""
    try:
        # Validação dos campos obrigatórios
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()

        errors = []

        if not name:
            errors.append('O campo "Nome" é obrigatório')

        if not email:
            errors.append('O campo "E-mail" é obrigatório')

        # Se houver erros de validação, retornar ao formulário com mensagens
        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('admin.user_edit', user_id=user_id))

        user_data = {
            'name': name,
            'email': email,
            'phone': request.form.get('phone'),
            'avatar': request.form.get('avatar'),
            'is_active': request.form.get('is_active', 'off') == 'on'
        }

        user = user_service.update_user(user_id, user_data)
        if user:
            flash('Usuário atualizado com sucesso!', 'success')
        else:
            flash('Usuário não encontrado', 'error')

        return redirect(url_for('admin.user_edit', user_id=user_id))
    except Exception as e:
        flash(f'Erro ao atualizar usuário: {str(e)}', 'error')
        return redirect(url_for('admin.user_edit', user_id=user_id))


def user_delete(user_id):
    """Remove um usuário"""
    try:
        if user_service.delete_user(user_id):
            flash('Usuário removido com sucesso!', 'success')
        else:
            flash('Usuário não encontrado', 'error')

        return redirect(url_for('admin.users_list'))
    except Exception as e:
        flash(f'Erro ao remover usuário: {str(e)}', 'error')
        return redirect(url_for('admin.users_list'))
