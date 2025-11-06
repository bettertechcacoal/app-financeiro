# -*- coding: utf-8 -*-
"""
Seeder de Veículos
Popula a tabela de veículos com dados de teste para a frota
"""
import sys
from config import ROOT_DIR

sys.path.insert(0, ROOT_DIR)

from app.models.database import SessionLocal
from app.models.vehicle import Vehicle
from datetime import datetime
from sqlalchemy import text


def seed_vehicles():
    """Cria veículos de teste para gestão da frota"""
    db = SessionLocal()

    try:

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

        for vehicle_data in vehicles_data:
            existing = db.query(Vehicle).filter(Vehicle.plate == vehicle_data['plate']).first()

            if not existing:
                # Criar veículo
                vehicle = Vehicle(**vehicle_data)
                db.add(vehicle)

        # Ajustar sequência de auto incremento do PostgreSQL
        db.execute(text("SELECT setval(pg_get_serial_sequence('vehicles', 'id'), (SELECT COALESCE(MAX(id), 1) FROM vehicles))"))
        db.commit()

        print("[SUCCESS] Seeder de veículos executado com sucesso")

    except Exception as e:
        db.rollback()
        print(f"[ERRO] {type(e).__name__}: {str(e).split(chr(10))[0]}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_vehicles()
