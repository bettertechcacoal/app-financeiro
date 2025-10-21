# -*- coding: utf-8 -*-
"""
Controller de Gerenciamento de Permissões
Gerencia permissões e associação de permissões a grupos
"""

from flask import render_template, request, redirect, url_for, flash, jsonify
from app.models.database import SessionLocal
from app.models.permission import Permission
from app.models.group import Group
from app.models.group_permission import group_permissions
from app.utils.permissions_helper import permission_required
from sqlalchemy import select, delete


@permission_required('permissions_view')
def permissions_list():
    """
    Lista todas as permissões do sistema agrupadas por módulo
    """
    db = SessionLocal()
    try:
        # Buscar todas as permissões ordenadas por módulo e nome
        permissions = db.query(Permission).order_by(Permission.module, Permission.name).all()

        # Agrupar por módulo
        permissions_by_module = {}
        for permission in permissions:
            module = permission.module or 'outros'
            if module not in permissions_by_module:
                permissions_by_module[module] = []
            permissions_by_module[module].append(permission)

        return render_template('admin/permissions/list.html',
                             permissions_by_module=permissions_by_module,
                             total_permissions=len(permissions))
    finally:
        db.close()


@permission_required('permissions_manage')
def groups_permissions():
    """
    Página de gerenciamento de permissões por grupo
    """
    db = SessionLocal()
    try:
        # Buscar todos os grupos
        groups = db.query(Group).order_by(Group.name).all()

        # Buscar todas as permissões agrupadas por módulo
        permissions = db.query(Permission).order_by(Permission.module, Permission.name).all()

        # Agrupar permissões por módulo
        permissions_by_module = {}
        for permission in permissions:
            module = permission.module or 'outros'
            if module not in permissions_by_module:
                permissions_by_module[module] = []
            permissions_by_module[module].append(permission)

        # Para cada grupo, carregar suas permissões
        for group in groups:
            _ = group.permissions_rel  # Força o carregamento

        return render_template('pages/permissions/groups.html',
                             groups=groups,
                             permissions_by_module=permissions_by_module)
    finally:
        db.close()


@permission_required('permissions_manage')
def group_permissions_update(group_id):
    """
    Atualiza as permissões de um grupo específico

    Args:
        group_id: ID do grupo
    """
    db = SessionLocal()
    try:
        # Buscar o grupo
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            flash('Grupo não encontrado', 'danger')
            return redirect(url_for('admin.groups_permissions'))

        # Obter IDs das permissões selecionadas do formulário
        permission_ids = request.form.getlist('permissions')
        permission_ids = [int(pid) for pid in permission_ids if pid.isdigit()]

        # Remover todas as permissões atuais do grupo
        db.execute(
            delete(group_permissions).where(group_permissions.c.group_id == group_id)
        )

        # Adicionar as novas permissões
        for permission_id in permission_ids:
            db.execute(
                group_permissions.insert().values(
                    group_id=group_id,
                    permission_id=permission_id
                )
            )

        db.commit()
        flash(f'Permissões do grupo "{group.name}" atualizadas com sucesso!', 'success')
        return redirect(url_for('admin.groups_permissions'))

    except Exception as e:
        db.rollback()
        flash(f'Erro ao atualizar permissões: {str(e)}', 'danger')
        return redirect(url_for('admin.groups_permissions'))
    finally:
        db.close()


@permission_required('permissions_manage')
def api_group_permissions(group_id):
    """
    API: Retorna as permissões de um grupo específico

    Args:
        group_id: ID do grupo

    Returns:
        JSON com lista de IDs das permissões do grupo
    """
    db = SessionLocal()
    try:
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            return jsonify({'error': 'Grupo não encontrado'}), 404

        # Retornar IDs das permissões
        permission_ids = [perm.id for perm in group.permissions_rel]

        return jsonify({
            'group_id': group.id,
            'group_name': group.name,
            'permission_ids': permission_ids
        })
    finally:
        db.close()


@permission_required('permissions_view')
def api_permissions_by_module():
    """
    API: Retorna todas as permissões agrupadas por módulo

    Returns:
        JSON com permissões agrupadas por módulo
    """
    db = SessionLocal()
    try:
        permissions = db.query(Permission).order_by(Permission.module, Permission.name).all()

        # Agrupar por módulo
        result = {}
        for permission in permissions:
            module = permission.module or 'outros'
            if module not in result:
                result[module] = []
            result[module].append({
                'id': permission.id,
                'name': permission.name,
                'slug': permission.slug,
                'description': permission.description
            })

        return jsonify(result)
    finally:
        db.close()
