# -*- coding: utf-8 -*-
"""
Seed para popular a tabela license_applications com mapeamento de códigos → módulos
Baseado no mapeamento real dos sistemas Elotech
"""
import sys
from config import ROOT_DIR

# Adicionar o diretorio raiz ao path
sys.path.insert(0, ROOT_DIR)

from app.models.database import SessionLocal
from app.models.license_application import LicenseApplication


def seed_license_applications():
    """Popula a tabela com os 22 módulos mapeados"""
    db = SessionLocal()

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

    try:
        inserted_count = 0
        updated_count = 0

        for module in modules:
            # Verificar se já existe
            existing = db.query(LicenseApplication).filter(
                LicenseApplication.code == module['code']
            ).first()

            if existing:
                # Atualizar se o nome mudou
                if existing.name != module['name']:
                    existing.name = module['name']
                    updated_count += 1
                    print(f"  [OK] Módulo atualizado: {module['code']} - {module['name']}")
                else:
                    print(f"  [OK] Módulo já existe: {module['code']} - {module['name']}")
            else:
                # Inserir novo
                app = LicenseApplication(
                    code=module['code'],
                    name=module['name']
                )
                db.add(app)
                inserted_count += 1
                print(f"  [OK] Módulo criado: {module['code']} - {module['name']}")

        db.commit()

        print(f"\n{'='*60}")
        print(f"Seeder finalizado com sucesso!")
        print(f"Módulos inseridos: {inserted_count}")
        print(f"Módulos atualizados: {updated_count}")
        print(f"Total de módulos: {len(modules)}")
        print(f"{'='*60}\n")

        return inserted_count + updated_count

    except Exception as e:
        db.rollback()
        print(f"\n[ERRO] Erro ao executar seeder: {str(e)}\n")
        raise e
    finally:
        db.close()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("SEEDER: License Applications (Módulos)")
    print("="*60 + "\n")
    seed_license_applications()
