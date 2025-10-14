# -*- coding: utf-8 -*-
"""
Seeder de Permissões
Popula a tabela permissions com todas as permissões do sistema
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

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
                'module': 'clientes'
            },
            {
                'name': 'Criar Cliente',
                'slug': 'clients_create',
                'description': 'Permite criar novos clientes',
                'module': 'clientes'
            },
            {
                'name': 'Editar Cliente',
                'slug': 'clients_edit',
                'description': 'Permite editar dados de clientes',
                'module': 'clientes'
            },
            {
                'name': 'Deletar Cliente',
                'slug': 'clients_delete',
                'description': 'Permite deletar clientes',
                'module': 'clientes'
            },
            {
                'name': 'Gerenciar Aplicações de Clientes',
                'slug': 'clients_manage_applications',
                'description': 'Permite vincular/desvincular aplicações aos clientes',
                'module': 'clientes'
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
                'slug': 'viagens_view',
                'description': 'Permite visualizar suas próprias viagens',
                'module': 'viagens'
            },
            {
                'name': 'Solicitar Viagem',
                'slug': 'viagens_create',
                'description': 'Permite criar solicitação de viagem',
                'module': 'viagens'
            },
            {
                'name': 'Editar Viagem',
                'slug': 'viagens_edit',
                'description': 'Permite editar suas próprias viagens',
                'module': 'viagens'
            },
            {
                'name': 'Deletar Viagem',
                'slug': 'viagens_delete',
                'description': 'Permite deletar suas próprias viagens',
                'module': 'viagens'
            },
            {
                'name': 'Aprovar Viagens',
                'slug': 'viagens_approve',
                'description': 'Permite aprovar ou reprovar viagens',
                'module': 'viagens'
            },
            {
                'name': 'Cancelar Viagens',
                'slug': 'viagens_cancel',
                'description': 'Permite cancelar viagens',
                'module': 'viagens'
            },
            {
                'name': 'Visualizar Todas Viagens',
                'slug': 'viagens_view_all',
                'description': 'Permite visualizar viagens de todos os usuários',
                'module': 'viagens'
            },

            # ===== FINANCEIRO (FINANCE) =====
            {
                'name': 'Visualizar Financeiro',
                'slug': 'financeiro_view',
                'description': 'Permite visualizar módulo financeiro',
                'module': 'financeiro'
            },
            {
                'name': 'Prestação de Contas',
                'slug': 'financeiro_prestacao_contas',
                'description': 'Permite acessar e gerenciar prestação de contas',
                'module': 'financeiro'
            },

            # ===== VEÍCULOS (VEHICLES) =====
            {
                'name': 'Visualizar Veículos',
                'slug': 'veiculos_view',
                'description': 'Permite visualizar lista de veículos',
                'module': 'veiculos'
            },
            {
                'name': 'Criar Veículo',
                'slug': 'veiculos_create',
                'description': 'Permite cadastrar novos veículos',
                'module': 'veiculos'
            },
            {
                'name': 'Editar Veículo',
                'slug': 'veiculos_edit',
                'description': 'Permite editar dados de veículos',
                'module': 'veiculos'
            },
            {
                'name': 'Deletar Veículo',
                'slug': 'veiculos_delete',
                'description': 'Permite deletar veículos',
                'module': 'veiculos'
            },
            {
                'name': 'Gerenciar Manutenções',
                'slug': 'veiculos_manage_maintenance',
                'description': 'Permite gerenciar manutenções de veículos',
                'module': 'veiculos'
            },

            # ===== INTEGRAÇÕES (INTEGRATIONS) =====
            {
                'name': 'Visualizar Integrações',
                'slug': 'integrations_view',
                'description': 'Permite visualizar página de integrações',
                'module': 'integracoes'
            },
            {
                'name': 'Gerenciar Integrações',
                'slug': 'integrations_manage',
                'description': 'Permite gerenciar todas as integrações',
                'module': 'integracoes'
            },
            {
                'name': 'Sincronizar Tickets Movidesk',
                'slug': 'integrations_sync_tickets',
                'description': 'Permite sincronizar tickets do Movidesk',
                'module': 'integracoes'
            },
            {
                'name': 'Sincronizar Organizações Movidesk',
                'slug': 'integrations_sync_organizations',
                'description': 'Permite sincronizar organizações do Movidesk',
                'module': 'integracoes'
            },
            {
                'name': 'Editar Organizações',
                'slug': 'integrations_edit_organizations',
                'description': 'Permite editar organizações integradas',
                'module': 'integracoes'
            },
            {
                'name': 'Vincular Clientes',
                'slug': 'integrations_link_clients',
                'description': 'Permite vincular/desvincular clientes de organizações',
                'module': 'integracoes'
            },

            # ===== LICENÇAS (LICENSES) =====
            {
                'name': 'Visualizar Licenças',
                'slug': 'licenses_view',
                'description': 'Permite visualizar licenças',
                'module': 'licencas'
            },
            {
                'name': 'Upload de Licenças',
                'slug': 'licenses_upload',
                'description': 'Permite fazer upload de licenças',
                'module': 'licencas'
            },
            {
                'name': 'Gerar Licenças',
                'slug': 'licenses_generate',
                'description': 'Permite gerar licenças',
                'module': 'licencas'
            },
            {
                'name': 'Gerar Licenças em Lote',
                'slug': 'licenses_generate_bulk',
                'description': 'Permite gerar múltiplas licenças',
                'module': 'licencas'
            },
            {
                'name': 'Visualizar PDF de Licenças',
                'slug': 'licenses_view_pdf',
                'description': 'Permite visualizar licenças em PDF',
                'module': 'licencas'
            },
            {
                'name': 'Deletar Data de Licença',
                'slug': 'licenses_delete_date',
                'description': 'Permite deletar datas de licenças',
                'module': 'licencas'
            },
            {
                'name': 'Gerenciar Módulos de Licenças',
                'slug': 'licenses_manage_modules',
                'description': 'Permite criar/editar módulos de licenças',
                'module': 'licencas'
            },

            # ===== USUÁRIOS (USERS) =====
            {
                'name': 'Visualizar Usuários',
                'slug': 'users_view',
                'description': 'Permite visualizar lista de usuários',
                'module': 'usuarios'
            },
            {
                'name': 'Criar Usuário',
                'slug': 'users_create',
                'description': 'Permite criar novos usuários',
                'module': 'usuarios'
            },
            {
                'name': 'Editar Usuário',
                'slug': 'users_edit',
                'description': 'Permite editar usuários',
                'module': 'usuarios'
            },
            {
                'name': 'Deletar Usuário',
                'slug': 'users_delete',
                'description': 'Permite deletar usuários',
                'module': 'usuarios'
            },
            {
                'name': 'Gerenciar Grupos de Usuários',
                'slug': 'users_manage_groups',
                'description': 'Permite gerenciar grupos dos usuários',
                'module': 'usuarios'
            },

            # ===== PERFIL (PROFILE) =====
            {
                'name': 'Visualizar Próprio Perfil',
                'slug': 'profile_view',
                'description': 'Permite visualizar próprio perfil',
                'module': 'perfil'
            },
            {
                'name': 'Editar Próprio Perfil',
                'slug': 'profile_edit',
                'description': 'Permite editar próprio perfil',
                'module': 'perfil'
            },

            # ===== NOTIFICAÇÕES (NOTIFICATIONS) =====
            {
                'name': 'Visualizar Notificações',
                'slug': 'notifications_view',
                'description': 'Permite visualizar notificações',
                'module': 'notificacoes'
            },
            {
                'name': 'Gerenciar Notificações',
                'slug': 'notifications_manage',
                'description': 'Permite marcar como lida e deletar notificações',
                'module': 'notificacoes'
            },

            # ===== CONFIGURAÇÕES (SETTINGS) =====
            {
                'name': 'Visualizar Configurações',
                'slug': 'settings_view',
                'description': 'Permite visualizar configurações do sistema',
                'module': 'configuracoes'
            },
            {
                'name': 'Editar Configurações',
                'slug': 'settings_edit',
                'description': 'Permite editar configurações do sistema',
                'module': 'configuracoes'
            },

            # ===== NOTAS (NOTES) =====
            {
                'name': 'Visualizar Notas',
                'slug': 'notes_view',
                'description': 'Permite visualizar notas/lembretes',
                'module': 'notas'
            },
            {
                'name': 'Criar Nota',
                'slug': 'notes_create',
                'description': 'Permite criar novas notas',
                'module': 'notas'
            },
            {
                'name': 'Editar Nota',
                'slug': 'notes_edit',
                'description': 'Permite editar notas',
                'module': 'notas'
            },
            {
                'name': 'Deletar Nota',
                'slug': 'notes_delete',
                'description': 'Permite deletar notas',
                'module': 'notas'
            },

            # ===== RELATÓRIOS (REPORTS) =====
            {
                'name': 'Visualizar Relatórios',
                'slug': 'reports_view',
                'description': 'Permite visualizar relatórios',
                'module': 'relatorios'
            },
            {
                'name': 'Gerar Relatórios',
                'slug': 'reports_generate',
                'description': 'Permite gerar relatórios em PDF',
                'module': 'relatorios'
            },
            {
                'name': 'Exportar Relatórios',
                'slug': 'reports_export',
                'description': 'Permite exportar relatórios',
                'module': 'relatorios'
            },

            # ===== PERMISSÕES (PERMISSIONS) - Gerenciamento =====
            {
                'name': 'Visualizar Permissões',
                'slug': 'permissions_view',
                'description': 'Permite visualizar permissões do sistema',
                'module': 'permissoes'
            },
            {
                'name': 'Gerenciar Permissões',
                'slug': 'permissions_manage',
                'description': 'Permite gerenciar permissões dos grupos',
                'module': 'permissoes'
            },

            # ===== GRUPOS (GROUPS) - Gerenciamento =====
            {
                'name': 'Visualizar Grupos',
                'slug': 'groups_view',
                'description': 'Permite visualizar grupos do sistema',
                'module': 'grupos'
            },
            {
                'name': 'Criar Grupo',
                'slug': 'groups_create',
                'description': 'Permite criar novos grupos',
                'module': 'grupos'
            },
            {
                'name': 'Editar Grupo',
                'slug': 'groups_edit',
                'description': 'Permite editar grupos',
                'module': 'grupos'
            },
            {
                'name': 'Deletar Grupo',
                'slug': 'groups_delete',
                'description': 'Permite deletar grupos',
                'module': 'grupos'
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
