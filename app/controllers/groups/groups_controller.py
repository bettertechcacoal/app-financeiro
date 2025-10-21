# -*- coding: utf-8 -*-
"""
Controller de Gerenciamento de Grupos
Gerencia a criação, edição e exclusão de grupos
"""

from flask import render_template, request, redirect, url_for, flash
from app.models.database import SessionLocal
from app.models.group import Group
from app.models.permission import Permission
from app.utils.permissions_helper import permission_required


@permission_required('groups_view')
def groups_list():
    """
    Lista todos os grupos do sistema
    """
    db = SessionLocal()
    try:
        groups = db.query(Group).order_by(Group.name).all()
        return render_template('pages/groups/list.html', groups=groups)
    finally:
        db.close()


@permission_required('groups_create')
def groups_create():
    """
    Exibe formulário de criação de grupo
    GET: Mostra o formulário
    POST: Cria o novo grupo
    """
    db = SessionLocal()
    try:
        if request.method == 'GET':
            # Buscar todas as permissões agrupadas por módulo
            permissions = db.query(Permission).order_by(Permission.module, Permission.name).all()

            # Agrupar permissões por módulo
            permissions_by_module = {}
            for permission in permissions:
                module = permission.module or 'outros'
                if module not in permissions_by_module:
                    permissions_by_module[module] = []
                permissions_by_module[module].append(permission)

            return render_template('pages/groups/create.html',
                                 permissions_by_module=permissions_by_module)

        # POST: Criar o grupo
        name = request.form.get('name', '').strip()
        slug = request.form.get('slug', '').strip()
        description = request.form.get('description', '').strip()
        color = request.form.get('color', '#3b82f6')
        icon = request.form.get('icon', 'fa-users')

        # Validações
        if not name or not slug:
            flash('Nome e slug são obrigatórios', 'danger')
            return redirect(url_for('admin.groups_create'))

        # Verificar se slug já existe
        existing = db.query(Group).filter(Group.slug == slug).first()
        if existing:
            flash(f'Já existe um grupo com o slug "{slug}"', 'danger')
            return redirect(url_for('admin.groups_create'))

        # Criar o grupo
        new_group = Group(
            name=name,
            slug=slug,
            description=description,
            color=color,
            icon=icon
        )
        db.add(new_group)
        db.flush()  # Para obter o ID

        # Adicionar permissões selecionadas
        permission_ids = request.form.getlist('permissions')
        if permission_ids:
            permissions = db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
            new_group.permissions_rel = permissions

        db.commit()
        flash(f'Grupo "{name}" criado com sucesso!', 'success')
        return redirect(url_for('admin.groups_permissions'))

    except Exception as e:
        db.rollback()
        flash(f'Erro ao criar grupo: {str(e)}', 'danger')
        return redirect(url_for('admin.groups_create'))
    finally:
        db.close()


@permission_required('groups_edit')
def groups_edit(group_id):
    """
    Exibe formulário de edição de grupo
    GET: Mostra o formulário
    POST: Atualiza o grupo
    """
    db = SessionLocal()
    try:
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            flash('Grupo não encontrado', 'danger')
            return redirect(url_for('admin.groups_permissions'))

        if request.method == 'GET':
            return render_template('pages/groups/edit.html', group=group)

        # POST: Atualizar o grupo
        group.name = request.form.get('name', '').strip()
        group.description = request.form.get('description', '').strip()
        group.color = request.form.get('color', '#3b82f6')
        group.icon = request.form.get('icon', 'fa-users')

        # Não permitir alterar slug (pode quebrar referências)

        db.commit()
        flash(f'Grupo "{group.name}" atualizado com sucesso!', 'success')
        return redirect(url_for('admin.groups_permissions'))

    except Exception as e:
        db.rollback()
        flash(f'Erro ao atualizar grupo: {str(e)}', 'danger')
        return redirect(url_for('admin.groups_edit', group_id=group_id))
    finally:
        db.close()


@permission_required('groups_delete')
def groups_delete(group_id):
    """
    Deleta um grupo
    """
    db = SessionLocal()
    try:
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            flash('Grupo não encontrado', 'danger')
            return redirect(url_for('admin.groups_permissions'))

        # Verificar se há usuários neste grupo
        if group.users:
            flash(f'Não é possível excluir o grupo "{group.name}" pois existem {len(group.users)} usuários vinculados', 'danger')
            return redirect(url_for('admin.groups_permissions'))

        group_name = group.name
        db.delete(group)
        db.commit()

        flash(f'Grupo "{group_name}" excluído com sucesso!', 'success')
        return redirect(url_for('admin.groups_permissions'))

    except Exception as e:
        db.rollback()
        flash(f'Erro ao excluir grupo: {str(e)}', 'danger')
        return redirect(url_for('admin.groups_permissions'))
    finally:
        db.close()
