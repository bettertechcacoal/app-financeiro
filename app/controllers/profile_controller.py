# -*- coding: utf-8 -*-
"""
Controller para gerenciar o perfil do usuário
"""
from flask import render_template, session, redirect, url_for, flash, request
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
