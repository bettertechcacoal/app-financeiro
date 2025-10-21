# -*- coding: utf-8 -*-
"""
Seeder para popular o banco de dados com viagens de teste
"""
import sys
from config import ROOT_DIR
from datetime import datetime, timedelta

# Adicionar o diretorio raiz ao path
sys.path.insert(0, ROOT_DIR)

from app.models.database import SessionLocal
from app.models.travel import Travel, TravelStatus
from app.models.travel_passenger import TravelPassenger
from app.models.user import User
from app.models.city import City


def seed_travels():
    """Popula o banco com viagens de teste"""

    db = SessionLocal()

    try:
        # Buscar usuários
        users = db.query(User).filter_by(active=True).all()

        if not users or len(users) == 0:
            print("\n[ERRO] Nenhum usuário encontrado!")
            print("Execute primeiro: python database/seeders/users_seeder.py")
            return

        # Buscar cidades
        cities = db.query(City).limit(10).all()

        if not cities or len(cities) == 0:
            print("\n[ERRO] Nenhuma cidade encontrada!")
            print("Execute primeiro: python database/seeders/cities_seeder.py")
            return

        # Usar o primeiro usuário como solicitante principal
        main_user = users[0]

        # Datas para as viagens
        today = datetime.now()

        # Definir viagens de teste
        travels_data = [
            {
                'user_id': main_user.id,
                'city_id': cities[0].id if len(cities) > 0 else None,
                'purpose': 'Reunião com Cliente',
                'departure_date': today + timedelta(days=3, hours=7, minutes=30),
                'return_date': today + timedelta(days=3, hours=18, minutes=0),
                'needs_vehicle': True,
                'status': TravelStatus.PENDING,
                'notes': 'Levar notebook e documentação do projeto',
                'passengers': []  # Sem passageiros
            },
            {
                'user_id': main_user.id,
                'city_id': cities[1].id if len(cities) > 1 else cities[0].id,
                'purpose': 'Treinamento Técnico',
                'departure_date': today + timedelta(days=7, hours=8, minutes=0),
                'return_date': today + timedelta(days=9, hours=17, minutes=0),
                'needs_vehicle': False,
                'status': TravelStatus.APPROVED,
                'notes': 'Confirmar hotel e transporte',
                'approved_at': today - timedelta(days=1),
                'passengers': [main_user.id] if len(users) > 0 else []  # Adicionar o próprio usuário como passageiro
            },
            {
                'user_id': main_user.id,
                'city_id': cities[2].id if len(cities) > 2 else cities[0].id,
                'purpose': 'Suporte Técnico On-site',
                'departure_date': today + timedelta(days=1, hours=6, minutes=0),
                'return_date': today + timedelta(days=1, hours=22, minutes=0),
                'needs_vehicle': True,
                'status': TravelStatus.APPROVED,
                'notes': 'Levar kit de ferramentas e equipamentos de backup',
                'approved_at': today - timedelta(hours=2),
                'passengers': []
            },
            {
                'user_id': main_user.id,
                'city_id': cities[3].id if len(cities) > 3 else cities[0].id,
                'purpose': 'Visita Técnica - Novo Projeto',
                'departure_date': today + timedelta(days=15, hours=9, minutes=0),
                'return_date': today + timedelta(days=15, hours=16, minutes=30),
                'needs_vehicle': True,
                'status': TravelStatus.PENDING,
                'notes': 'Agendar reunião com gerente de TI do cliente',
                'passengers': []
            },
            {
                'user_id': main_user.id,
                'city_id': cities[4].id if len(cities) > 4 else cities[0].id,
                'purpose': 'Workshop de Integração',
                'departure_date': today - timedelta(days=5, hours=-8, minutes=0),
                'return_date': today - timedelta(days=5, hours=-17, minutes=0),
                'needs_vehicle': False,
                'status': TravelStatus.COMPLETED,
                'notes': 'Material didático fornecido pela empresa',
                'approved_at': today - timedelta(days=10),
                'passengers': []
            }
        ]

        created_count = 0
        existing_count = 0

        for travel_data in travels_data:
            # Verifica se a viagem já existe (por propósito e data)
            existing_travel = db.query(Travel).filter_by(
                purpose=travel_data['purpose'],
                departure_date=travel_data['departure_date']
            ).first()

            if not existing_travel:
                # Extrair dados de passageiros
                passengers = travel_data.pop('passengers', [])
                approved_at = travel_data.pop('approved_at', None)

                # Criar viagem
                travel = Travel(**travel_data)

                if approved_at:
                    travel.approved_at = approved_at

                db.add(travel)
                db.flush()  # Para obter o ID da viagem

                # Adicionar passageiros
                for passenger_user_id in passengers:
                    passenger = TravelPassenger(
                        travel_id=travel.id,
                        user_id=passenger_user_id
                    )
                    db.add(passenger)

                created_count += 1
                city_name = db.query(City).filter_by(id=travel_data['city_id']).first().name
                print(f"  [OK] Viagem criada: {travel_data['purpose']} -> {city_name} ({travel_data['status'].value})")
            else:
                existing_count += 1
                print(f"  [OK] Viagem já existe: {travel_data['purpose']}")

        db.commit()

        print(f"\n{'='*60}")
        print(f"Seeder finalizado com sucesso!")
        print(f"Viagens criadas: {created_count}")
        print(f"Viagens já existentes: {existing_count}")
        print(f"Total de viagens: {len(travels_data)}")
        print(f"{'='*60}\n")

        # Mostrar resumo
        print("Resumo de Viagens Criadas:")
        travels = db.query(Travel).order_by(Travel.created_at.desc()).limit(created_count).all()
        for travel in travels:
            city = db.query(City).filter_by(id=travel.city_id).first()
            print(f"  - {travel.purpose}")
            print(f"    Destino: {city.name if city else 'N/A'}")
            print(f"    Data: {travel.departure_date.strftime('%d/%m/%Y %H:%M')}")
            print(f"    Status: {travel.status.value}")
            print(f"    Veículo: {'Sim' if travel.needs_vehicle else 'Não'}")
            passengers_count = len(travel.travel_passengers) if travel.travel_passengers else 0
            print(f"    Passageiros: {passengers_count}")
            print()

    except Exception as e:
        db.rollback()
        print(f"\n[ERRO] Erro ao executar seeder: {str(e)}\n")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("SEEDER: Viagens de Teste")
    print("="*60 + "\n")
    seed_travels()
