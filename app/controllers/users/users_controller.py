# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, jsonify
from app.services.user_service import user_service
from app.services.group_service import group_service
from app.services.auth_service import auth_service


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
        password = request.form.get('password', '').strip()

        errors = []

        if not name:
            errors.append('O campo "Nome" é obrigatório')

        if not email:
            errors.append('O campo "E-mail" é obrigatório')

        if not password:
            errors.append('O campo "Senha" é obrigatório')

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
            'active': request.form.get('active', 'on') == 'on',
            'groups': request.form.getlist('groups[]')  # Capturar grupos selecionados
        }

        # Primeiro cria usuário localmente para obter sid_uuid
        user = user_service.create_user(user_data)

        # Tenta sincronizar com auth-service
        auth_response = auth_service.register_user(user, password)

        if not auth_response:
            # Se falhar na API, deleta o usuário local (rollback)
            user_service.delete_user(user['id'])
            flash('Erro ao criar usuário no serviço de autenticação. O usuário não foi criado.', 'error')
            return redirect(url_for('admin.user_new'))

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
            'active': request.form.get('active', 'off') == 'on',
            'groups': request.form.getlist('groups[]')  # Capturar grupos selecionados
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


def get_users_api():
    """API para buscar todos os usuários"""
    try:
        users = user_service.get_all_users()

        # Retornar todos os usuários - o filtro do solicitante é feito no frontend
        return jsonify({'success': True, 'clients': users})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def user_change_password(user_id):
    """Altera a senha de um usuário"""
    try:
        # Validar se é uma requisição JSON
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Requisição inválida'}), 400

        data = request.get_json()
        new_password = data.get('new_password', '').strip()

        # Validações
        if not new_password:
            return jsonify({'success': False, 'error': 'A nova senha é obrigatória'}), 400

        if len(new_password) < 8:
            return jsonify({'success': False, 'error': 'A senha deve ter no mínimo 8 caracteres'}), 400

        # Buscar usuário
        user = user_service.get_user_by_id(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'Usuário não encontrado'}), 404

        # Tentar alterar senha no auth-service
        auth_response = auth_service.change_password(user['sid_uuid'], new_password)

        if not auth_response:
            return jsonify({'success': False, 'error': 'Erro ao alterar senha no serviço de autenticação'}), 500

        return jsonify({'success': True, 'message': 'Senha alterada com sucesso!'}), 200

    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro ao alterar senha: {str(e)}'}), 500
