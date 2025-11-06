# -*- coding: utf-8 -*-
"""
Controller para gerenciar o perfil do usuário
"""
from flask import render_template, session, redirect, url_for, flash, request, jsonify
from app.models.database import SessionLocal
from app.models.user import User


def profile_view():
    """Exibe a página de perfil do usuário"""

    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar esta página', 'warning')
        return redirect(url_for('auth.login'))

    db = SessionLocal()

    try:
        # Buscar usuário no banco
        user = db.query(User).filter_by(id=session['user_id']).first()

        if not user:
            flash('Usuário não encontrado', 'error')
            return redirect(url_for('auth.logout'))

        # Buscar grupos do usuário
        from app.models.user_group import user_groups as user_groups_table
        from app.models.group import Group

        user_groups = db.query(Group).join(
            user_groups_table, user_groups_table.c.group_id == Group.id
        ).filter(
            user_groups_table.c.user_id == user.id
        ).all()

        # Converter para dict
        user_data = user.to_dict()
        user_data['groups'] = [group.to_dict() for group in user_groups]

        return render_template('pages/profile/profile.html', user=user_data, is_admin_edit=False, is_new=False)

    except Exception as e:
        print(f"Erro ao carregar perfil: {str(e)}")
        flash('Erro ao carregar perfil do usuário', 'error')
        return redirect(url_for('admin.dashboard'))
    finally:
        db.close()


def profile_update():
    """Atualiza os dados do perfil do usuário"""

    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar esta página', 'warning')
        return redirect(url_for('auth.login'))

    db = SessionLocal()

    try:
        # Buscar usuário no banco
        user = db.query(User).filter_by(id=session['user_id']).first()

        if not user:
            flash('Usuário não encontrado', 'error')
            return redirect(url_for('auth.logout'))

        # Atualizar dados
        user.name = request.form.get('name', user.name)
        user.email = request.form.get('email', user.email)
        user.phone = request.form.get('phone', user.phone)

        db.commit()

        # Atualizar sessão
        session['user_name'] = user.name
        session['user_email'] = user.email

        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('admin.profile_view'))

    except Exception as e:
        db.rollback()
        print(f"Erro ao atualizar perfil: {str(e)}")
        flash('Erro ao atualizar perfil', 'error')
        return redirect(url_for('admin.profile_view'))
    finally:
        db.close()


def profile_change_password():
    """Altera a senha do usuário logado"""
    try:
        # Validar se o usuário está logado
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Você precisa estar logado'}), 401

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

        # Buscar usuário logado
        from app.services import user_service, auth_service

        user = user_service.get_user_by_id(session['user_id'])
        if not user:
            return jsonify({'success': False, 'error': 'Usuário não encontrado'}), 404

        # Alterar senha no auth-service
        auth_response = auth_service.change_password(user['sid_uuid'], new_password)

        if not auth_response:
            return jsonify({'success': False, 'error': 'Erro ao alterar senha no serviço de autenticação'}), 500

        return jsonify({'success': True, 'message': 'Senha alterada com sucesso!'}), 200

    except Exception as e:
        print(f"Erro ao alterar senha: {str(e)}")
        return jsonify({'success': False, 'error': f'Erro ao alterar senha: {str(e)}'}), 500
