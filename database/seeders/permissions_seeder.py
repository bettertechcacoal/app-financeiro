# -*- coding: utf-8 -*-
"""
Seeder de Permissões
Popula a tabela permissions com todas as permissões do sistema
"""

import sys
from config import ROOT_DIR

# Adicionar o diretório raiz ao path
sys.path.insert(0, ROOT_DIR)

from app.models.database import SessionLocal
from app.models.permission import Permission
from sqlalchemy import text


def seed_permissions():
    """Popula a tabela de permissões com todas as permissões do sistema"""
    db = SessionLocal()

    try:
        print("[SEEDER] Iniciando seed de permissões...")

        # Limpar permissões existentes
        db.execute(text("DELETE FROM permissions"))
        db.commit()

        # Lista completa de permissões organizadas por módulo
        permissions_data = [
            # ===== DASHBOARD =====
            {
                'name': 'Visualizar Dashboard',
                'slug': 'dashboard_view',
                'description': 'Permite visualizar o dashboard principal',
                'module': 'dashboard'
            },

            # ===== CLIENTES (CLIENTS/ORGANIZATIONS) =====
            {
                'name': 'Visualizar Clientes',
                'slug': 'clients_view',
                'description': 'Permite visualizar lista de clientes',
                'module': 'clients'
            },
            {
                'name': 'Criar Cliente',
                'slug': 'clients_create',
                'description': 'Permite criar novos clientes',
                'module': 'clients'
            },
            {
                'name': 'Editar Cliente',
                'slug': 'clients_edit',
                'description': 'Permite editar dados de clientes',
                'module': 'clients'
            },
            {
                'name': 'Deletar Cliente',
                'slug': 'clients_delete',
                'description': 'Permite deletar clientes',
                'module': 'clients'
            },
            {
                'name': 'Gerenciar Aplicações de Clientes',
                'slug': 'clients_manage_applications',
                'description': 'Permite vincular/desvincular aplicações aos clientes',
                'module': 'clients'
            },

            # ===== TICKETS =====
            {
                'name': 'Visualizar Tickets',
                'slug': 'tickets_view',
                'description': 'Permite visualizar lista de tickets',
                'module': 'tickets'
            },
            {
                'name': 'Visualizar Tickets de Cliente',
                'slug': 'tickets_view_client',
                'description': 'Permite visualizar tickets de cliente específico',
                'module': 'tickets'
            },
            {
                'name': 'Criar Ticket',
                'slug': 'tickets_create',
                'description': 'Permite criar novos tickets',
                'module': 'tickets'
            },
            {
                'name': 'Editar Ticket',
                'slug': 'tickets_edit',
                'description': 'Permite editar tickets',
                'module': 'tickets'
            },
            {
                'name': 'Deletar Ticket',
                'slug': 'tickets_delete',
                'description': 'Permite deletar tickets',
                'module': 'tickets'
            },
            {
                'name': 'Gerenciar Todos os Tickets',
                'slug': 'tickets_manage_all',
                'description': 'Permite gerenciar todos os tickets do sistema',
                'module': 'tickets'
            },

            # ===== VIAGENS (TRAVELS) =====
            {
                'name': 'Visualizar Viagens',
                'slug': 'travels_view',
                'description': 'Permite visualizar suas próprias viagens',
                'module': 'travels'
            },
            {
                'name': 'Solicitar Viagem',
                'slug': 'travels_create',
                'description': 'Permite criar solicitação de viagem',
                'module': 'travels'
            },
            {
                'name': 'Editar Viagem',
                'slug': 'travels_edit',
                'description': 'Permite editar suas próprias viagens',
                'module': 'travels'
            },
            {
                'name': 'Deletar Viagem',
                'slug': 'travels_delete',
                'description': 'Permite deletar suas próprias viagens',
                'module': 'travels'
            },
            {
                'name': 'Aprovar Viagens',
                'slug': 'travels_approve',
                'description': 'Permite aprovar ou reprovar viagens',
                'module': 'travels'
            },
            {
                'name': 'Cancelar Viagens',
                'slug': 'travels_cancel',
                'description': 'Permite cancelar viagens',
                'module': 'travels'
            },
            {
                'name': 'Lançar Viagem Retroativa',
                'slug': 'travels_create_retroactive',
                'description': 'Permite criar viagens com datas retroativas (passadas)',
                'module': 'travels'
            },
            {
                'name': 'Visualizar Todas Viagens',
                'slug': 'travels_view_all',
                'description': 'Permite visualizar viagens de todos os usuários',
                'module': 'travels'
            },

            # ===== FINANCEIRO (FINANCE) =====
            {
                'name': 'Visualizar Financeiro',
                'slug': 'financial_view',
                'description': 'Permite visualizar módulo financeiro',
                'module': 'financial'
            },
            {
                'name': 'Prestação de Contas',
                'slug': 'financial_accountability',
                'description': 'Permite acessar e gerenciar prestação de contas',
                'module': 'financial'
            },
            {
                'name': 'Analisar Prestação de Contas',
                'slug': 'financial_review_accountability',
                'description': 'Permite analisar, aprovar ou devolver prestações de contas enviadas',
                'module': 'financial'
            },

            # ===== VEÍCULOS (VEHICLES) =====
            {
                'name': 'Visualizar Veículos',
                'slug': 'vehicles_view',
                'description': 'Permite visualizar lista de veículos',
                'module': 'vehicles'
            },
            {
                'name': 'Criar Veículo',
                'slug': 'vehicles_create',
                'description': 'Permite cadastrar novos veículos',
                'module': 'vehicles'
            },
            {
                'name': 'Editar Veículo',
                'slug': 'vehicles_edit',
                'description': 'Permite editar dados de veículos',
                'module': 'vehicles'
            },
            {
                'name': 'Deletar Veículo',
                'slug': 'vehicles_delete',
                'description': 'Permite deletar veículos',
                'module': 'vehicles'
            },
            {
                'name': 'Gerenciar Manutenções',
                'slug': 'vehicles_manage_maintenance',
                'description': 'Permite gerenciar manutenções de veículos',
                'module': 'vehicles'
            },

            # ===== INTEGRAÇÕES (INTEGRATIONS) =====
            {
                'name': 'Visualizar Integrações',
                'slug': 'integrations_view',
                'description': 'Permite visualizar página de integrações',
                'module': 'integrations'
            },
            {
                'name': 'Gerenciar Integrações',
                'slug': 'integrations_manage',
                'description': 'Permite gerenciar todas as integrações',
                'module': 'integrations'
            },
            {
                'name': 'Sincronizar Tickets Movidesk',
                'slug': 'integrations_sync_tickets',
                'description': 'Permite sincronizar tickets do Movidesk',
                'module': 'integrations'
            },
            {
                'name': 'Sincronizar Organizações Movidesk',
                'slug': 'integrations_sync_organizations',
                'description': 'Permite sincronizar organizações do Movidesk',
                'module': 'integrations'
            },
            {
                'name': 'Editar Organizações',
                'slug': 'integrations_edit_organizations',
                'description': 'Permite editar organizações integradas',
                'module': 'integrations'
            },
            {
                'name': 'Vincular Clientes',
                'slug': 'integrations_link_clients',
                'description': 'Permite vincular/desvincular clientes de organizações',
                'module': 'integrations'
            },

            # ===== LICENÇAS (LICENSES) =====
            {
                'name': 'Visualizar Licenças',
                'slug': 'licenses_view',
                'description': 'Permite visualizar licenças',
                'module': 'licenses'
            },
            {
                'name': 'Upload de Licenças',
                'slug': 'licenses_upload',
                'description': 'Permite fazer upload de licenças',
                'module': 'licenses'
            },
            {
                'name': 'Gerar Licenças',
                'slug': 'licenses_generate',
                'description': 'Permite gerar licenças',
                'module': 'licenses'
            },
            {
                'name': 'Gerar Licenças em Lote',
                'slug': 'licenses_generate_bulk',
                'description': 'Permite gerar múltiplas licenças',
                'module': 'licenses'
            },
            {
                'name': 'Visualizar PDF de Licenças',
                'slug': 'licenses_view_pdf',
                'description': 'Permite visualizar licenças em PDF',
                'module': 'licenses'
            },
            {
                'name': 'Deletar Data de Licença',
                'slug': 'licenses_delete_date',
                'description': 'Permite deletar datas de licenças',
                'module': 'licenses'
            },
            {
                'name': 'Gerenciar Módulos de Licenças',
                'slug': 'licenses_manage_modules',
                'description': 'Permite criar/editar módulos de licenças',
                'module': 'licenses'
            },

            # ===== USUÁRIOS (USERS) =====
            {
                'name': 'Visualizar Usuários',
                'slug': 'users_view',
                'description': 'Permite visualizar lista de usuários',
                'module': 'users'
            },
            {
                'name': 'Criar Usuário',
                'slug': 'users_create',
                'description': 'Permite criar novos usuários',
                'module': 'users'
            },
            {
                'name': 'Editar Usuário',
                'slug': 'users_edit',
                'description': 'Permite editar usuários',
                'module': 'users'
            },
            {
                'name': 'Deletar Usuário',
                'slug': 'users_delete',
                'description': 'Permite deletar usuários',
                'module': 'users'
            },
            {
                'name': 'Gerenciar Grupos de Usuários',
                'slug': 'users_manage_groups',
                'description': 'Permite gerenciar grupos dos usuários',
                'module': 'users'
            },

            # ===== PERFIL (PROFILE) =====
            {
                'name': 'Visualizar Próprio Perfil',
                'slug': 'profile_view',
                'description': 'Permite visualizar próprio perfil',
                'module': 'profile'
            },
            {
                'name': 'Editar Próprio Perfil',
                'slug': 'profile_edit',
                'description': 'Permite editar próprio perfil',
                'module': 'profile'
            },

            # ===== NOTIFICAÇÕES (NOTIFICATIONS) =====
            {
                'name': 'Visualizar Notificações',
                'slug': 'notifications_view',
                'description': 'Permite visualizar notificações',
                'module': 'notifications'
            },
            {
                'name': 'Gerenciar Notificações',
                'slug': 'notifications_manage',
                'description': 'Permite marcar como lida e deletar notificações',
                'module': 'notifications'
            },

            # ===== CONFIGURAÇÕES (SETTINGS) =====
            {
                'name': 'Visualizar Configurações',
                'slug': 'settings_view',
                'description': 'Permite visualizar configurações do sistema',
                'module': 'settings'
            },
            {
                'name': 'Editar Configurações',
                'slug': 'settings_edit',
                'description': 'Permite editar configurações do sistema',
                'module': 'settings'
            },

            # ===== NOTAS (NOTES) =====
            {
                'name': 'Visualizar Notas',
                'slug': 'notes_view',
                'description': 'Permite visualizar notas/lembretes',
                'module': 'notes'
            },
            {
                'name': 'Criar Nota',
                'slug': 'notes_create',
                'description': 'Permite criar novas notas',
                'module': 'notes'
            },
            {
                'name': 'Editar Nota',
                'slug': 'notes_edit',
                'description': 'Permite editar notas',
                'module': 'notes'
            },
            {
                'name': 'Deletar Nota',
                'slug': 'notes_delete',
                'description': 'Permite deletar notas',
                'module': 'notes'
            },

            # ===== RELATÓRIOS (REPORTS) =====
            {
                'name': 'Visualizar Relatórios',
                'slug': 'reports_view',
                'description': 'Permite visualizar relatórios',
                'module': 'reports'
            },
            {
                'name': 'Gerar Relatórios',
                'slug': 'reports_generate',
                'description': 'Permite gerar relatórios em PDF',
                'module': 'reports'
            },
            {
                'name': 'Exportar Relatórios',
                'slug': 'reports_export',
                'description': 'Permite exportar relatórios',
                'module': 'reports'
            },

            # ===== PERMISSÕES (PERMISSIONS) - Gerenciamento =====
            {
                'name': 'Visualizar Permissões',
                'slug': 'permissions_view',
                'description': 'Permite visualizar permissões do sistema',
                'module': 'permissions'
            },
            {
                'name': 'Gerenciar Permissões',
                'slug': 'permissions_manage',
                'description': 'Permite gerenciar permissões dos grupos',
                'module': 'permissions'
            },

            # ===== GRUPOS (GROUPS) - Gerenciamento =====
            {
                'name': 'Visualizar Grupos',
                'slug': 'groups_view',
                'description': 'Permite visualizar grupos do sistema',
                'module': 'groups'
            },
            {
                'name': 'Criar Grupo',
                'slug': 'groups_create',
                'description': 'Permite criar novos grupos',
                'module': 'groups'
            },
            {
                'name': 'Editar Grupo',
                'slug': 'groups_edit',
                'description': 'Permite editar grupos',
                'module': 'groups'
            },
            {
                'name': 'Deletar Grupo',
                'slug': 'groups_delete',
                'description': 'Permite deletar grupos',
                'module': 'groups'
            },
        ]

        # Inserir permissões
        for perm_data in permissions_data:
            permission = Permission(**perm_data)
            db.add(permission)

        db.commit()
        print(f"[SUCCESS] {len(permissions_data)} permissões foram criadas com sucesso!")

        # Mostrar resumo por módulo
        print("\n[INFO] Permissões criadas por módulo:")
        modules = {}
        for perm in permissions_data:
            module = perm['module']
            if module not in modules:
                modules[module] = 0
            modules[module] += 1

        for module, count in sorted(modules.items()):
            print(f"  - {module}: {count} permissões")

    except Exception as e:
        print(f"[ERROR] Erro ao criar permissões: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == '__main__':
    seed_permissions()
