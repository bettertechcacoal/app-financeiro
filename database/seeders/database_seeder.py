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
from travels_seeder import seed_travels


def seed_database():
    """Executa todos os seeders na ordem correta"""

    print("\n" + "="*60)
    print("INICIANDO SEEDERS DO BANCO DE DADOS")
    print("="*60 + "\n")

    try:
        # 1. Seeder de Grupos
        print("[1/4] Executando seeder de Groups...")
        seed_groups()

        # 2. Seeder de Usuarios
        print("[2/4] Executando seeder de Users...")
        seed_users()

        # 3. Seeder de Cidades de Rondonia
        print("[3/4] Executando seeder de Cities (Rondonia)...")
        seed_rondonia_cities()

        # 4. Seeder de Viagens
        print("[4/4] Executando seeder de Travels...")
        seed_travels()

        print("\n" + "="*60)
        print("TODOS OS SEEDERS FORAM EXECUTADOS COM SUCESSO!")
        print("="*60 + "\n")

        print("Resumo:")
        print("  [OK] Groups: 4 grupos criados")
        print("  [OK] Users: 1 usuario criado (demo@demo.com)")
        print("  [OK] User-Groups: 1 vinculo criado")
        print("  [OK] States: 1 estado (Rondonia)")
        print("  [OK] Cities: 52 cidades de Rondonia")
        print("  [OK] Travels: 5 viagens de teste criadas")
        print()

    except Exception as e:
        print("\n" + "="*60)
        print("ERRO AO EXECUTAR SEEDERS!")
        print("="*60)
        print(f"\nErro: {str(e)}\n")
        raise


if __name__ == '__main__':
    seed_database()
