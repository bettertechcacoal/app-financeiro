# -*- coding: utf-8 -*-
"""
Seeder Master - Executa todos os seeders na ordem correta

Modos de execução:
  - production: Apenas dados essenciais (grupos, cidades, clientes reais, parâmetros)
  - development: Dados essenciais + dados de teste (usuários, viagens, etc)

Uso:
  python database_seeder.py production
  python database_seeder.py development
  python database_seeder.py  (padrão: development)
"""
import sys
import os
import argparse

# Adicionar o diretorio raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importar funcoes dos seeders
from groups_seeder import seed_groups
from users_seeder import seed_users
from cities_seeder import seed_rondonia_cities
from clients_seeder import seed_clients
from applications_seeder import seed_applications
from client_applications_seeder import seed_client_applications
from travels_seeder import seed_travels
from notifications_seeder import seed_notifications
from parameter_groups_seeder import seed_parameter_groups
from parameters_seeder import seed_parameters
from vehicles_seeder import seed
from permissions_seeder import seed_permissions
from group_permissions_seeder import seed_group_permissions
from maintenance_types_seeder import seed_maintenance_types


def seed_production():
    """Executa apenas seeders essenciais para produção"""

    print("\n" + "="*60)
    print("MODO: PRODUÇÃO")
    print("INICIANDO SEEDERS ESSENCIAIS DO BANCO DE DADOS")
    print("="*60 + "\n")

    try:
        # 1. Seeder de Grupos (ESSENCIAL)
        print("[1/8] Executando seeder de Groups...")
        seed_groups()

        # 2. Seeder de Permissões (ESSENCIAL)
        print("[2/8] Executando seeder de Permissions...")
        seed_permissions()

        # 3. Seeder de Atribuição de Permissões aos Grupos (ESSENCIAL)
        print("[3/8] Executando atribuição de permissões aos grupos...")
        seed_group_permissions()

        # 4. Seeder de Cidades de Rondonia (ESSENCIAL)
        print("[4/8] Executando seeder de Cities (Rondonia)...")
        seed_rondonia_cities()

        # 5. Seeder de Clientes Reais (ESSENCIAL - PRODUÇÃO)
        print("[5/8] Executando seeder de Clients (PRODUÇÃO)...")
        seed_clients()

        # 6. Seeder de Tipos de Manutenção (ESSENCIAL)
        print("[6/8] Executando seeder de Maintenance Types...")
        seed_maintenance_types()

        # 7. Seeder de Grupos de Parâmetros (ESSENCIAL)
        print("[7/8] Executando seeder de Parameter Groups...")
        seed_parameter_groups()

        # 8. Seeder de Parâmetros (ESSENCIAL)
        print("[8/8] Executando seeder de Parameters...")
        seed_parameters()

        print("\n" + "="*60)
        print("SEEDERS ESSENCIAIS EXECUTADOS COM SUCESSO!")
        print("="*60 + "\n")

        print("Resumo:")
        print("  [OK] Groups: 4 grupos criados (Administradores, Gestores, Colaboradores, Visitantes)")
        print("  [OK] Permissions: 67 permissões criadas")
        print("  [OK] Group Permissions: Permissões atribuídas aos grupos")
        print("       - Administradores: Todas as permissões")
        print("       - Gestores: Permissões de gestão")
        print("       - Colaboradores: Permissões básicas")
        print("       - Visitantes: Somente visualização")
        print("  [OK] States: 1 estado (Rondonia)")
        print("  [OK] Cities: 52 cidades de Rondonia")
        print("  [OK] Clients: 33 clientes municipais de Rondônia")
        print("       - Prefeituras, Câmaras, SAAE, Institutos de Previdência")
        print("  [OK] Maintenance Types: 15 tipos de manutenção criados")
        print("  [OK] Parameter Groups: 4 grupos criados")
        print("  [OK] Parameters: 12 parâmetros criados")
        print()
        print("IMPORTANTE: Em produção, você deve criar manualmente:")
        print("  - Usuários administrativos (via interface ou Auth-Service)")
        print("  - Aplicações do sistema")
        print("  - Veículos da frota")
        print("  - Configurações específicas da empresa")
        print()

    except Exception as e:
        print("\n" + "="*60)
        print("ERRO AO EXECUTAR SEEDERS!")
        print("="*60)
        print(f"\nErro: {str(e)}\n")
        raise


def seed_development():
    """Executa todos os seeders incluindo dados de teste"""

    print("\n" + "="*60)
    print("MODO: DESENVOLVIMENTO")
    print("INICIANDO SEEDERS DO BANCO DE DADOS (INCLUINDO DADOS DE TESTE)")
    print("="*60 + "\n")

    try:
        # SEEDERS ESSENCIAIS

        # 1. Seeder de Grupos
        print("[1/11] Executando seeder de Groups...")
        seed_groups()

        # 2. Seeder de Usuarios (TESTE)
        print("[2/11] Executando seeder de Users (TESTE)...")
        seed_users()

        # 3. Seeder de Cidades de Rondonia
        print("[3/11] Executando seeder de Cities (Rondonia)...")
        seed_rondonia_cities()

        # SEEDERS DE TESTE

        # 4. Seeder de Clientes (TESTE)
        print("[4/11] Executando seeder de Clients (TESTE)...")
        seed_clients()

        # 5. Seeder de Aplicações (TESTE)
        print("[5/11] Executando seeder de Applications (TESTE)...")
        seed_applications()

        # 6. Seeder de Associações Cliente-Aplicação (TESTE)
        print("[6/11] Executando seeder de Client Applications (TESTE)...")
        seed_client_applications()

        # 7. Seeder de Viagens (TESTE)
        print("[7/11] Executando seeder de Travels (TESTE)...")
        seed_travels()

        # 8. Seeder de Notificações (TESTE)
        print("[8/11] Executando seeder de Notifications (TESTE)...")
        seed_notifications()

        # 9. Seeder de Grupos de Parâmetros
        print("[9/11] Executando seeder de Parameter Groups...")
        seed_parameter_groups()

        # 10. Seeder de Parâmetros
        print("[10/11] Executando seeder de Parameters...")
        seed_parameters()

        # 11. Seeder de Veículos (TESTE)
        print("[11/11] Executando seeder de Vehicles (TESTE)...")
        seed()

        print("\n" + "="*60)
        print("TODOS OS SEEDERS FORAM EXECUTADOS COM SUCESSO!")
        print("="*60 + "\n")

        print("Resumo:")
        print("  [OK] Groups: 4 grupos criados")
        print("  [OK] Users: 1 usuario de teste criado (demo@demo.com)")
        print("  [OK] User-Groups: 1 vinculo criado")
        print("  [OK] States: 1 estado (Rondonia)")
        print("  [OK] Cities: 52 cidades de Rondonia")
        print("  [OK] Clients: 33 clientes de teste criados")
        print("  [OK] Applications: 22 aplicações de teste criadas")
        print("  [OK] Client Applications: Associações de teste criadas")
        print("  [OK] Travels: 5 viagens de teste criadas")
        print("  [OK] Notifications: 8 notificações de teste criadas")
        print("  [OK] Parameter Groups: 4 grupos criados")
        print("  [OK] Parameters: 12 parâmetros criados")
        print("  [OK] Vehicles: Veículos de teste criados")
        print()
        print("ATENÇÃO: Este modo incluiu dados de teste!")
        print("Não utilize em produção.")
        print()

    except Exception as e:
        print("\n" + "="*60)
        print("ERRO AO EXECUTAR SEEDERS!")
        print("="*60)
        print(f"\nErro: {str(e)}\n")
        raise


def main():
    """Função principal com suporte a argumentos de linha de comando"""
    parser = argparse.ArgumentParser(
        description='Seeder do banco de dados - Suporta modo produção e desenvolvimento',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python database_seeder.py production      # Apenas dados essenciais
  python database_seeder.py development     # Dados essenciais + dados de teste
  python database_seeder.py                 # Padrão: development
        """
    )

    parser.add_argument(
        'mode',
        nargs='?',
        choices=['production', 'development'],
        default='development',
        help='Modo de execução: production (apenas essencial) ou development (com dados de teste)'
    )

    args = parser.parse_args()

    if args.mode == 'production':
        seed_production()
    else:
        seed_development()


if __name__ == '__main__':
    main()
