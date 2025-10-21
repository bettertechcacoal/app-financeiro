# -*- coding: utf-8 -*-
"""
Seeder Master - Executa todos os seeders na ordem correta

Uso:
  python database_seeder.py production
  python database_seeder.py development
"""
import sys
import os
import argparse
import contextlib

# Adicionar o diretorio raiz ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, ROOT_DIR)

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
from vehicles_seeder import seed_vehicles
from permissions_seeder import seed_permissions
from group_permissions_seeder import seed_group_permissions
from maintenance_types_seeder import seed_maintenance_types
from license_applications_seeder import seed_license_applications


@contextlib.contextmanager
def suppress_output():
    """Suprime a saída padrão temporariamente"""
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def seed_production():
    """Executa apenas seeders essenciais para produção"""

    seeders = [
        ('GroupsSeeder', seed_groups),
        ('PermissionsSeeder', seed_permissions),
        ('GroupPermissionsSeeder', seed_group_permissions),
        ('UsersSeeder', seed_users),
        ('CitiesSeeder', seed_rondonia_cities),
        ('ClientsSeeder', seed_clients),
        ('ApplicationsSeeder', seed_applications),
        ('LicenseApplicationsSeeder', seed_license_applications),
        ('ClientApplicationsSeeder', seed_client_applications),
        ('MaintenanceTypesSeeder', seed_maintenance_types),
        ('ParameterGroupsSeeder', seed_parameter_groups),
        ('ParametersSeeder', seed_parameters),
    ]

    print("\nSeeding: Production")

    for name, seeder_func in seeders:
        with suppress_output():
            seeder_func()
        print(f"  [OK] {name}")

    print("\nDatabase seeding completed successfully.\n")


def seed_development():
    """Executa todos os seeders incluindo dados de teste"""

    seeders = [
        ('GroupsSeeder', seed_groups),
        ('PermissionsSeeder', seed_permissions),
        ('GroupPermissionsSeeder', seed_group_permissions),
        ('UsersSeeder', seed_users),
        ('CitiesSeeder', seed_rondonia_cities),
        ('ClientsSeeder', seed_clients),
        ('ApplicationsSeeder', seed_applications),
        ('ClientApplicationsSeeder', seed_client_applications),
        ('TravelsSeeder', seed_travels),
        ('NotificationsSeeder', seed_notifications),
        ('MaintenanceTypesSeeder', seed_maintenance_types),
        ('ParameterGroupsSeeder', seed_parameter_groups),
        ('ParametersSeeder', seed_parameters),
        ('VehiclesSeeder', seed_vehicles),
    ]

    print("\nSeeding: Development")

    for name, seeder_func in seeders:
        with suppress_output():
            seeder_func()
        print(f"  [OK] {name}")

    print("\nDatabase seeding completed successfully.\n")


def main():
    """Função principal com suporte a argumentos de linha de comando"""
    parser = argparse.ArgumentParser(description='Database seeder')

    parser.add_argument(
        'mode',
        nargs='?',
        choices=['production', 'development'],
        default='development',
        help='Seeding mode'
    )

    args = parser.parse_args()

    try:
        if args.mode == 'production':
            seed_production()
        else:
            seed_development()
    except Exception as e:
        print(f"\n[ERRO] Error: {str(e)}\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
