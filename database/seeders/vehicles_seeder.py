# -*- coding: utf-8 -*-
"""
Seeder: Vehicles
Popula a tabela de veículos com dados de teste
"""

import sys
import os

# Adicionar o diretorio raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import SessionLocal
from app.models.vehicle import Vehicle
from datetime import datetime


def seed():
    """Popula a tabela vehicles com dados de teste"""
    db = SessionLocal()

    try:
        print("\n[SEEDER] Criando veículos de teste...")

        vehicles_data = [
            {
                'plate': 'ABC-1234',
                'brand': 'Volkswagen',
                'model': 'Gol',
                'year': 2020,
                'is_active': True
            },
            {
                'plate': 'DEF-5678',
                'brand': 'Fiat',
                'model': 'Uno',
                'year': 2019,
                'is_active': True
            },
            {
                'plate': 'GHI-9012',
                'brand': 'Chevrolet',
                'model': 'Onix',
                'year': 2021,
                'is_active': True
            },
            {
                'plate': 'JKL-3456',
                'brand': 'Toyota',
                'model': 'Corolla',
                'year': 2022,
                'is_active': True
            },
            {
                'plate': 'MNO-7890',
                'brand': 'Honda',
                'model': 'Civic',
                'year': 2018,
                'is_active': False
            },
            {
                'plate': 'PQR-1122',
                'brand': 'Renault',
                'model': 'Sandero',
                'year': 2020,
                'is_active': True
            },
            {
                'plate': 'STU-3344',
                'brand': 'Ford',
                'model': 'Ka',
                'year': 2019,
                'is_active': True
            },
            {
                'plate': 'VWX-5566',
                'brand': 'Hyundai',
                'model': 'HB20',
                'year': 2021,
                'is_active': True
            }
        ]

        created_count = 0
        existing_count = 0

        for vehicle_data in vehicles_data:
            # Verificar se já existe
            existing = db.query(Vehicle).filter(Vehicle.plate == vehicle_data['plate']).first()

            if not existing:
                vehicle = Vehicle(**vehicle_data)
                db.add(vehicle)
                created_count += 1
                print(f"  [OK] Veículo criado: {vehicle_data['plate']} - {vehicle_data['brand']} {vehicle_data['model']}")
            else:
                existing_count += 1
                print(f"  [OK] Veículo já existe: {vehicle_data['plate']}")

        db.commit()

        print("\n" + "="*60)
        print("Seeder finalizado com sucesso!")
        print(f"Veículos criados: {created_count}")
        print(f"Veículos já existentes: {existing_count}")
        print(f"Total de veículos: {created_count + existing_count}")
        print("="*60)

    except Exception as e:
        db.rollback()
        print(f"\n[ERRO] Falha ao executar seeder: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
