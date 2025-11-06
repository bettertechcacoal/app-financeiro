# -*- coding: utf-8 -*-
"""
Seeder de Permissões de Grupos
Atribui permissões padrão aos grupos de acesso do sistema
"""
import sys
from config import ROOT_DIR

sys.path.insert(0, ROOT_DIR)

from app.models.database import SessionLocal
from app.models.group import Group
from app.models.permission import Permission


def seed_group_permissions():
    """Vincula permissões padrão aos grupos de acesso do sistema"""
    db = SessionLocal()

    try:
        # Configurar grupo Administradores
        admin_group = db.query(Group).filter(Group.slug == 'administradores').first()
        if admin_group:
            all_permissions = db.query(Permission).all()
            admin_group.permissions_rel = all_permissions

        # Configurar grupo Gestores
        manager_group = db.query(Group).filter(Group.slug == 'gestores').first()
        if manager_group:
            manager_permission_slugs = [
                # Dashboard
                'dashboard_view',

                # Clientes
                'clients_view',
                'clients_create',
                'clients_edit',
                'clients_manage_applications',

                # Tickets
                'tickets_view',
                'tickets_view_client',
                'tickets_create',
                'tickets_edit',
                'tickets_manage_all',

                # Viagens - Gerente pode visualizar todas e aprovar
                'travels_view',
                'travels_view_all',
                'travels_create',
                'travels_create_retroactive',
                'travels_approve',
                'travels_cancel',

                # Financeiro
                'financial_view',
                'financial_accountability',

                # Veículos
                'vehicles_view',
                'vehicles_create',
                'vehicles_edit',
                'vehicles_delete',
                'vehicles_manage_maintenance',

                # Integrações
                'integrations_view',
                'integrations_sync_tickets',
                'integrations_sync_organizations',
                'integrations_edit_organizations',
                'integrations_link_clients',

                # Licenças
                'licenses_view',
                'licenses_generate',
                'licenses_view_pdf',

                # Usuários - Gerente pode visualizar
                'users_view',

                # Perfil
                'profile_view',
                'profile_edit',

                # Notificações
                'notifications_view',
                'notifications_manage',

                # Configurações - Apenas visualizar
                'settings_view',

                # Notas
                'notes_view',
                'notes_create',
                'notes_edit',
                'notes_delete',
            ]

            manager_permissions = db.query(Permission).filter(
                Permission.slug.in_(manager_permission_slugs)
            ).all()
            manager_group.permissions_rel = manager_permissions

        # Configurar grupo Colaboradores
        collab_group = db.query(Group).filter(Group.slug == 'colaboradores').first()
        if collab_group:
            collab_permission_slugs = [
                # Dashboard
                'dashboard_view',

                # Clientes - Apenas visualizar
                'clients_view',

                # Tickets - Básico
                'tickets_view',
                'tickets_view_client',
                'tickets_create',

                # Viagens - Apenas as suas próprias
                'travels_view',
                'travels_create',
                'travels_edit',

                # Financeiro - Apenas visualizar
                'financial_view',

                # Veículos - Apenas visualizar
                'vehicles_view',

                # Perfil
                'profile_view',
                'profile_edit',

                # Notificações
                'notifications_view',
                'notifications_manage',

                # Notas - Pessoais
                'notes_view',
                'notes_create',
                'notes_edit',
                'notes_delete',
            ]

            collab_permissions = db.query(Permission).filter(
                Permission.slug.in_(collab_permission_slugs)
            ).all()
            collab_group.permissions_rel = collab_permissions

        # Configurar grupo Visitantes
        visitor_group = db.query(Group).filter(Group.slug == 'visitantes').first()
        if visitor_group:
            visitor_permission_slugs = [
                'dashboard_view',
                'profile_view',
                'notifications_view',
            ]

            visitor_permissions = db.query(Permission).filter(
                Permission.slug.in_(visitor_permission_slugs)
            ).all()
            visitor_group.permissions_rel = visitor_permissions

        db.commit()

        print("[SUCCESS] Seeder de permissões de grupos executado com sucesso")

    except Exception as e:
        db.rollback()
        print(f"[ERRO] {type(e).__name__}: {str(e).split(chr(10))[0]}")
    finally:
        db.close()


if __name__ == '__main__':
    seed_group_permissions()
