# -*- coding: utf-8 -*-
"""
Script para Atribuir Permissões Padrão aos Grupos
Configura permissões adequadas para cada grupo do sistema
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import SessionLocal
from app.models.group import Group
from app.models.permission import Permission


def assign_group_permissions():
    """Atribui permissões padrão aos grupos do sistema"""
    db = SessionLocal()

    try:
        print("[SEEDER] Iniciando atribuição de permissões aos grupos...")

        # ========== GRUPO: ADMINISTRADORES ==========
        print("\n[INFO] Configurando grupo: Administradores...")
        admin_group = db.query(Group).filter(Group.slug == 'administradores').first()
        if admin_group:
            # Administradores têm TODAS as permissões
            all_permissions = db.query(Permission).all()
            admin_group.permissions_rel = all_permissions
            print(f"  ✓ {len(all_permissions)} permissões atribuídas aos Administradores")
        else:
            print("  ✗ Grupo 'administradores' não encontrado!")

        # ========== GRUPO: GESTORES ==========
        print("\n[INFO] Configurando grupo: Gestores...")
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
                'viagens_view',
                'viagens_view_all',
                'viagens_create',
                'viagens_approve',
                'viagens_cancel',

                # Financeiro
                'financeiro_view',
                'financeiro_prestacao_contas',

                # Veículos
                'veiculos_view',
                'veiculos_create',
                'veiculos_edit',
                'veiculos_delete',
                'veiculos_manage_maintenance',

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

                # Relatórios
                'reports_view',
                'reports_generate',
                'reports_export',
            ]

            manager_permissions = db.query(Permission).filter(
                Permission.slug.in_(manager_permission_slugs)
            ).all()
            manager_group.permissions_rel = manager_permissions
            print(f"  ✓ {len(manager_permissions)} permissões atribuídas aos Gestores")
        else:
            print("  ✗ Grupo 'gestores' não encontrado!")

        # ========== GRUPO: COLABORADORES ==========
        print("\n[INFO] Configurando grupo: Colaboradores...")
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
                'viagens_view',
                'viagens_create',
                'viagens_edit',

                # Financeiro - Apenas visualizar
                'financeiro_view',

                # Veículos - Apenas visualizar
                'veiculos_view',

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

                # Relatórios - Apenas visualizar
                'reports_view',
            ]

            collab_permissions = db.query(Permission).filter(
                Permission.slug.in_(collab_permission_slugs)
            ).all()
            collab_group.permissions_rel = collab_permissions
            print(f"  ✓ {len(collab_permissions)} permissões atribuídas aos Colaboradores")
        else:
            print("  ✗ Grupo 'colaboradores' não encontrado!")

        # ========== GRUPO: VISITANTES ==========
        print("\n[INFO] Configurando grupo: Visitantes...")
        visitor_group = db.query(Group).filter(Group.slug == 'visitantes').first()
        if visitor_group:
            visitor_permission_slugs = [
                # Dashboard
                'dashboard_view',

                # Perfil - Apenas visualizar
                'profile_view',

                # Notificações - Apenas visualizar
                'notifications_view',
            ]

            visitor_permissions = db.query(Permission).filter(
                Permission.slug.in_(visitor_permission_slugs)
            ).all()
            visitor_group.permissions_rel = visitor_permissions
            print(f"  ✓ {len(visitor_permissions)} permissões atribuídas aos Visitantes")
        else:
            print("  ✗ Grupo 'visitantes' não encontrado!")

        db.commit()
        print("\n[SUCCESS] Permissões atribuídas aos grupos com sucesso!\n")

        # Mostrar resumo
        print("=" * 60)
        print("RESUMO DAS PERMISSÕES POR GRUPO")
        print("=" * 60)

        all_groups = db.query(Group).order_by(Group.name).all()
        for group in all_groups:
            perm_count = len(group.permissions_rel)
            print(f"{group.name:20} | {perm_count:3} permissões")

        print("=" * 60)

    except Exception as e:
        print(f"\n[ERROR] Erro ao atribuir permissões: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == '__main__':
    assign_group_permissions()
