# -*- coding: utf-8 -*-
"""
Helper de Permissões
Funções auxiliares e decorators para verificação de permissões
"""

from functools import wraps
from flask import session, redirect, url_for, flash, abort
from app.models.database import SessionLocal
from app.models.user import User


def get_current_user():
    """
    Retorna o usuário atual da sessão com seus grupos e permissões carregados
    """
    if 'user_id' not in session:
        return None

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == session['user_id']).first()
        if user:
            # Forçar o carregamento dos relacionamentos antes de fechar a sessão
            _ = user.groups  # Carrega os grupos
            for group in user.groups:
                _ = group.permissions_rel  # Carrega as permissões de cada grupo
        return user
    finally:
        db.close()


def user_has_permission(permission_slug):
    """
    Verifica se o usuário atual possui uma permissão específica

    Args:
        permission_slug: Slug da permissão a verificar (ex: 'travels_create')

    Returns:
        bool: True se o usuário possui a permissão, False caso contrário
    """
    user = get_current_user()
    if not user:
        return False

    return user.has_permission(permission_slug)


def user_has_any_permission(permission_slugs):
    """
    Verifica se o usuário atual possui pelo menos uma das permissões especificadas

    Args:
        permission_slugs: Lista de slugs de permissões

    Returns:
        bool: True se o usuário possui pelo menos uma permissão, False caso contrário
    """
    user = get_current_user()
    if not user:
        return False

    return user.has_any_permission(permission_slugs)


def user_has_all_permissions(permission_slugs):
    """
    Verifica se o usuário atual possui todas as permissões especificadas

    Args:
        permission_slugs: Lista de slugs de permissões

    Returns:
        bool: True se o usuário possui todas as permissões, False caso contrário
    """
    user = get_current_user()
    if not user:
        return False

    return user.has_all_permissions(permission_slugs)


def permission_required(permission_slug, redirect_to='admin.dashboard'):
    """
    Decorator para proteger rotas que requerem uma permissão específica

    Usage:
        @permission_required('travels_create')
        def create_travel():
            # código da rota

    Args:
        permission_slug: Slug da permissão necessária
        redirect_to: Rota para redirecionar em caso de falta de permissão
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Primeiro verifica se está autenticado
            if 'user_id' not in session:
                flash('Você precisa estar logado para acessar esta página', 'warning')
                return redirect(url_for('auth.login'))

            # Verifica se tem a permissão
            if not user_has_permission(permission_slug):
                flash('Você não tem permissão para acessar esta funcionalidade', 'danger')
                return redirect(url_for(redirect_to))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def any_permission_required(permission_slugs, redirect_to='admin.dashboard'):
    """
    Decorator para proteger rotas que requerem pelo menos uma das permissões especificadas

    Usage:
        @any_permission_required(['travels_view', 'travels_view_all'])
        def list_travels():
            # código da rota

    Args:
        permission_slugs: Lista de slugs de permissões (usuário precisa ter pelo menos uma)
        redirect_to: Rota para redirecionar em caso de falta de permissão
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Primeiro verifica se está autenticado
            if 'user_id' not in session:
                flash('Você precisa estar logado para acessar esta página', 'warning')
                return redirect(url_for('auth.login'))

            # Verifica se tem pelo menos uma das permissões
            if not user_has_any_permission(permission_slugs):
                flash('Você não tem permissão para acessar esta funcionalidade', 'danger')
                return redirect(url_for(redirect_to))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def all_permissions_required(permission_slugs, redirect_to='admin.dashboard'):
    """
    Decorator para proteger rotas que requerem todas as permissões especificadas

    Usage:
        @all_permissions_required(['users_view', 'users_edit'])
        def edit_user():
            # código da rota

    Args:
        permission_slugs: Lista de slugs de permissões (usuário precisa ter todas)
        redirect_to: Rota para redirecionar em caso de falta de permissão
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Primeiro verifica se está autenticado
            if 'user_id' not in session:
                flash('Você precisa estar logado para acessar esta página', 'warning')
                return redirect(url_for('auth.login'))

            # Verifica se tem todas as permissões
            if not user_has_all_permissions(permission_slugs):
                flash('Você não tem permissão para acessar esta funcionalidade', 'danger')
                return redirect(url_for(redirect_to))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def inject_user_permissions():
    """
    Context processor para injetar as permissões do usuário nos templates
    Deve ser registrado no app Flask

    Usage no app:
        app.context_processor(inject_user_permissions)

    Usage no template:
        {% if 'travels_create' in user_permissions %}
            <button>Criar Viagem</button>
        {% endif %}
    """
    user = get_current_user()
    if user:
        return {
            'user_permissions': user.get_all_permissions(),
            'current_user': user
        }
    return {
        'user_permissions': [],
        'current_user': None
    }
