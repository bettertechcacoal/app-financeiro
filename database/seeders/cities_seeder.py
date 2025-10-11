# -*- coding: utf-8 -*-
"""
Seeder para popular o banco de dados com o estado de Rondonia e suas 52 cidades
"""
import sys
import os

# Adicionar o diretorio raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import SessionLocal
from app.models.state import State
from app.models.city import City
from app.models.travel import Travel  # Importar para registrar no SQLAlchemy
from app.models.user import User  # Importar para registrar no SQLAlchemy
from app.models.user_group import user_groups  # Importar tabela pivot para registrar no SQLAlchemy


def seed_rondonia_cities():
    """Popula o banco com o estado de Rondonia e suas 52 cidades"""

    db = SessionLocal()

    try:
        # Verifica se o estado ja existe
        state = db.query(State).filter_by(uf='RO').first()

        if not state:
            # Cria o estado de Rondonia
            state = State(
                name='Rondonia',
                uf='RO',
                ibge_code='11'
            )
            db.add(state)
            db.commit()
            print(f"[OK] Estado criado: {state.name}")
        else:
            print(f"[OK] Estado ja existe: {state.name}")

        # Lista das 52 cidades de Rondonia com seus codigos IBGE
        cities_data = [
            {'name': 'Alta Floresta d\'Oeste', 'ibge_code': '1100015'},
            {'name': 'Alto Alegre dos Parecis', 'ibge_code': '1100379'},
            {'name': 'Alto Paraiso', 'ibge_code': '1100403'},
            {'name': 'Alvorada d\'Oeste', 'ibge_code': '1100346'},
            {'name': 'Ariquemes', 'ibge_code': '1100023'},
            {'name': 'Buritis', 'ibge_code': '1100452'},
            {'name': 'Cabixi', 'ibge_code': '1100031'},
            {'name': 'Cacaulandia', 'ibge_code': '1100601'},
            {'name': 'Cacoal', 'ibge_code': '1100049'},
            {'name': 'Campo Novo de Rondonia', 'ibge_code': '1100700'},
            {'name': 'Candeias do Jamari', 'ibge_code': '1100809'},
            {'name': 'Castanheiras', 'ibge_code': '1100908'},
            {'name': 'Cerejeiras', 'ibge_code': '1100056'},
            {'name': 'Chupinguaia', 'ibge_code': '1100924'},
            {'name': 'Colorado do Oeste', 'ibge_code': '1100064'},
            {'name': 'Corumbiara', 'ibge_code': '1100072'},
            {'name': 'Costa Marques', 'ibge_code': '1100080'},
            {'name': 'Cujubim', 'ibge_code': '1100940'},
            {'name': 'Espigao d\'Oeste', 'ibge_code': '1100098'},
            {'name': 'Governador Jorge Teixeira', 'ibge_code': '1101005'},
            {'name': 'Guajara-Mirim', 'ibge_code': '1100106'},
            {'name': 'Itapua do Oeste', 'ibge_code': '1101104'},
            {'name': 'Jaru', 'ibge_code': '1100114'},
            {'name': 'Ji-Parana', 'ibge_code': '1100122'},
            {'name': 'Machadinho d\'Oeste', 'ibge_code': '1100130'},
            {'name': 'Ministro Andreazza', 'ibge_code': '1101203'},
            {'name': 'Mirante da Serra', 'ibge_code': '1101302'},
            {'name': 'Monte Negro', 'ibge_code': '1101401'},
            {'name': 'Nova Brasilandia d\'Oeste', 'ibge_code': '1100148'},
            {'name': 'Nova Mamore', 'ibge_code': '1100338'},
            {'name': 'Nova Uniao', 'ibge_code': '1101435'},
            {'name': 'Novo Horizonte do Oeste', 'ibge_code': '1100502'},
            {'name': 'Ouro Preto do Oeste', 'ibge_code': '1100155'},
            {'name': 'Parecis', 'ibge_code': '1101450'},
            {'name': 'Pimenta Bueno', 'ibge_code': '1100189'},
            {'name': 'Pimenteiras do Oeste', 'ibge_code': '1101468'},
            {'name': 'Porto Velho', 'ibge_code': '1100205'},
            {'name': 'Presidente Medici', 'ibge_code': '1100254'},
            {'name': 'Primavera de Rondonia', 'ibge_code': '1101476'},
            {'name': 'Rio Crespo', 'ibge_code': '1100262'},
            {'name': 'Rolim de Moura', 'ibge_code': '1100288'},
            {'name': 'Santa Luzia d\'Oeste', 'ibge_code': '1100296'},
            {'name': 'Sao Felipe d\'Oeste', 'ibge_code': '1101484'},
            {'name': 'Sao Francisco do Guapore', 'ibge_code': '1101492'},
            {'name': 'Sao Miguel do Guapore', 'ibge_code': '1100320'},
            {'name': 'Seringueiras', 'ibge_code': '1101500'},
            {'name': 'Teixeiropolis', 'ibge_code': '1101559'},
            {'name': 'Theobroma', 'ibge_code': '1101609'},
            {'name': 'Urupa', 'ibge_code': '1101708'},
            {'name': 'Vale do Anari', 'ibge_code': '1101757'},
            {'name': 'Vale do Paraiso', 'ibge_code': '1101807'},
            {'name': 'Vilhena', 'ibge_code': '1100304'}
        ]

        created_count = 0
        existing_count = 0

        for city_data in cities_data:
            # Verifica se a cidade ja existe
            existing_city = db.query(City).filter_by(ibge_code=city_data['ibge_code']).first()

            if not existing_city:
                city = City(
                    name=city_data['name'],
                    ibge_code=city_data['ibge_code'],
                    state_id=state.id
                )
                db.add(city)
                created_count += 1
                print(f"  [OK] Cidade criada: {city_data['name']}")
            else:
                existing_count += 1

        db.commit()

        print(f"\n{'='*60}")
        print(f"Seeder finalizado com sucesso!")
        print(f"Estado: Rondonia (RO)")
        print(f"Cidades criadas: {created_count}")
        print(f"Cidades ja existentes: {existing_count}")
        print(f"Total de cidades: {len(cities_data)}")
        print(f"{'='*60}\n")

    except Exception as e:
        db.rollback()
        print(f"\n[ERRO] Erro ao executar seeder: {str(e)}\n")
        raise
    finally:
        db.close()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("SEEDER: Cidades de Rondonia")
    print("="*60 + "\n")
    seed_rondonia_cities()
