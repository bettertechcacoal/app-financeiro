# -*- coding: utf-8 -*-
"""
Seeder de Aplicações de Licença
Popula a tabela de módulos de licença com códigos e nomes dos sistemas Elotech
"""
import sys
from config import ROOT_DIR

sys.path.insert(0, ROOT_DIR)

from app.models.database import SessionLocal
from app.models.license_application import LicenseApplication
from sqlalchemy import text


def seed_license_applications():
    """Cria módulos de licença com mapeamento de códigos para sistemas Elotech"""
    db = SessionLocal()

    try:
        # Mapeamento completo de códigos para módulos
        modules = [
        {'code': '002', 'name': 'APICE - Orçamento'},
        {'code': '003', 'name': 'APICE - Contabilidade'},
        {'code': '004', 'name': 'APICE - Protocolo'},
        {'code': '007', 'name': 'APICE - Patrimonio'},
        {'code': '008', 'name': 'APICE - Frotas'},
        {'code': '010', 'name': 'APICE - Compras e Licitações'},
        {'code': '011', 'name': 'APICE - SigEloAM'},
        {'code': '015', 'name': 'APICE - Tesouraria'},
        {'code': '019', 'name': 'APICE - Almoxarifado'},
        {'code': '025', 'name': 'AISE - Controle de Obras'},
        {'code': '026', 'name': 'WEB - Issqn'},
        {'code': '034', 'name': 'Portal Transparencia'},
        {'code': '035', 'name': 'WEB - Tributos'},
        {'code': '038', 'name': 'WEB - Cemitério'},
        {'code': '040', 'name': 'WEB - Alvará Online'},
        {'code': '042', 'name': 'WEB - Portal RH'},
        {'code': '063', 'name': 'OXY - ITBI Online'},
        {'code': '064', 'name': 'OXY - Cidadão APP - Mobile'},
        {'code': '065', 'name': 'OXY - Custos'},
        {'code': '101', 'name': 'AISE - Folha de Pagamento RH'},
        {'code': '306', 'name': 'AISE - Tributos'},
    ]

        # Criar ou atualizar módulos
        for module in modules:
            existing = db.query(LicenseApplication).filter(
                LicenseApplication.code == module['code']
            ).first()

            if existing:
                # Atualizar se o nome mudou
                if existing.name != module['name']:
                    existing.name = module['name']
            else:
                # Inserir novo
                app = LicenseApplication(
                    code=module['code'],
                    name=module['name']
                )
                db.add(app)

        # Ajustar sequência de auto incremento do PostgreSQL
        db.execute(text("SELECT setval(pg_get_serial_sequence('license_applications', 'id'), (SELECT COALESCE(MAX(id), 1) FROM license_applications))"))
        db.commit()

        print("[SUCCESS] Seeder de aplicações de licença executado com sucesso")

    except Exception as e:
        db.rollback()
        print(f"[ERRO] {type(e).__name__}: {str(e).split(chr(10))[0]}")
    finally:
        db.close()


if __name__ == '__main__':
    seed_license_applications()
