# -*- coding: utf-8 -*-
"""
Seeder Master - Executa todos os seeders na ordem correta
"""
import sys
import os

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


def seed_database():
    """Executa todos os seeders na ordem correta"""

    print("\n" + "="*60)
    print("INICIANDO SEEDERS DO BANCO DE DADOS")
    print("="*60 + "\n")

    try:
        # 1. Seeder de Grupos
        print("[1/10] Executando seeder de Groups...")
        seed_groups()

        # 2. Seeder de Usuarios
        print("[2/10] Executando seeder de Users...")
        seed_users()

        # 3. Seeder de Cidades de Rondonia
        print("[3/10] Executando seeder de Cities (Rondonia)...")
        seed_rondonia_cities()

        # 4. Seeder de Clientes
        print("[4/10] Executando seeder de Clients...")
        seed_clients()

        # 5. Seeder de Aplicações
        print("[5/10] Executando seeder de Applications...")
        seed_applications()

        # 6. Seeder de Associações Cliente-Aplicação
        print("[6/10] Executando seeder de Client Applications...")
        seed_client_applications()

        # 7. Seeder de Viagens
        print("[7/10] Executando seeder de Travels...")
        seed_travels()

        # 8. Seeder de Notificações
        print("[8/10] Executando seeder de Notifications...")
        seed_notifications()

        # 9. Seeder de Grupos de Parâmetros
        print("[9/10] Executando seeder de Parameter Groups...")
        seed_parameter_groups()

        # 10. Seeder de Parâmetros
        print("[10/10] Executando seeder de Parameters...")
        seed_parameters()

        print("\n" + "="*60)
        print("TODOS OS SEEDERS FORAM EXECUTADOS COM SUCESSO!")
        print("="*60 + "\n")

        print("Resumo:")
        print("  [OK] Groups: 4 grupos criados")
        print("  [OK] Users: 1 usuario criado (demo@demo.com)")
        print("  [OK] User-Groups: 1 vinculo criado")
        print("  [OK] States: 1 estado (Rondonia)")
        print("  [OK] Cities: 52 cidades de Rondonia")
        print("  [OK] Clients: 33 clientes municipais criados")
        print("  [OK] Applications: 22 aplicações criadas")
        print("  [OK] Client Applications: Associações cliente-aplicação criadas")
        print("  [OK] Travels: 5 viagens de teste criadas")
        print("  [OK] Notifications: 8 notificações de teste criadas")
        print("  [OK] Parameter Groups: 4 grupos criados")
        print("  [OK] Parameters: 12 parâmetros criados")
        print()

    except Exception as e:
        print("\n" + "="*60)
        print("ERRO AO EXECUTAR SEEDERS!")
        print("="*60)
        print(f"\nErro: {str(e)}\n")
        raise


if __name__ == '__main__':
    seed_database()
