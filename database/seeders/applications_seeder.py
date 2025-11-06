# -*- coding: utf-8 -*-
"""
Seeder para popular o banco de dados com aplicações/módulos
"""
import sys
from config import ROOT_DIR

# Adicionar o diretorio raiz ao path
sys.path.insert(0, ROOT_DIR)

from app.models.database import SessionLocal
from app.models.application import Application


def seed_applications():
    """Popula o banco com aplicações/módulos"""

    db = SessionLocal()

    try:
        # Lista de todos os módulos/aplicações únicos encontrados no arquivo clientes-sistemas.txt
        applications_data = [
            {'name': 'APICE - Orçamento', 'category': 'APICE', 'description': 'Sistema de Orçamento'},
            {'name': 'APICE- Contabilidade', 'category': 'APICE', 'description': 'Sistema de Contabilidade'},
            {'name': 'APICE-Protocolo', 'category': 'APICE', 'description': 'Sistema de Protocolo'},
            {'name': 'APICE-Patrimonio', 'category': 'APICE', 'description': 'Sistema de Patrimônio'},
            {'name': 'APICE-Frotas', 'category': 'APICE', 'description': 'Sistema de Frotas'},
            {'name': 'APICE - SigEloAM', 'category': 'APICE', 'description': 'Sistema de Gestão Eleitoral'},
            {'name': 'APICE-Tesouraria', 'category': 'APICE', 'description': 'Sistema de Tesouraria'},
            {'name': 'APICE- Almoxarifado', 'category': 'APICE', 'description': 'Sistema de Almoxarifado'},
            {'name': 'APICE- Compras e Licitações  ', 'category': 'APICE', 'description': 'Sistema de Compras e Licitações'},
            {'name': 'AISE- Controle de Obras', 'category': 'AISE', 'description': 'Sistema de Controle de Obras'},
            {'name': 'AISE-  Folha de Pagamento RH', 'category': 'AISE', 'description': 'Sistema de Folha de Pagamento'},
            {'name': 'AISE -Tributos ', 'category': 'AISE', 'description': 'Sistema de Tributos'},
            {'name': 'Portal Transparencia', 'category': 'Portal', 'description': 'Portal da Transparência'},
            {'name': 'WEB - Issqn', 'category': 'WEB', 'description': 'Sistema Web de ISSQN'},
            {'name': 'WEB - Tributos ', 'category': 'WEB', 'description': 'Sistema Web de Tributos'},
            {'name': 'WEB - Cemitério', 'category': 'WEB', 'description': 'Sistema Web de Cemitério'},
            {'name': 'WEB - Alvará Online', 'category': 'WEB', 'description': 'Sistema Web de Alvará Online'},
            {'name': 'WEB- Portal RH', 'category': 'WEB', 'description': 'Portal Web de Recursos Humanos'},
            {'name': 'OXY- Cidadão APP- Mobile ', 'category': 'OXY', 'description': 'Aplicativo Mobile do Cidadão'},
            {'name': 'OXY - Custos ', 'category': 'OXY', 'description': 'Sistema de Custos'},
            {'name': 'OXY - Cidadão ITBI Online', 'category': 'OXY', 'description': 'Sistema Online de ITBI'},
            {'name': 'OXY Folha de Pagamento', 'category': 'OXY', 'description': 'Sistema de Folha de Pagamento OXY'},
        ]

        created_count = 0
        existing_count = 0

        for idx, app_data in enumerate(applications_data, start=1):
            # Verifica se a aplicação ja existe pelo ID ou nome
            existing_app = db.query(Application).filter_by(id=idx).first()
            if not existing_app:
                existing_app = db.query(Application).filter_by(name=app_data['name']).first()

            if not existing_app:
                # Criar nova aplicação com ID fixo
                application = Application(
                    id=idx,
                    name=app_data['name'],
                    category=app_data.get('category'),
                    description=app_data.get('description'),
                    is_active=True
                )
                db.add(application)
                created_count += 1
                print(f"  [OK] Aplicação criada (ID={idx}): {app_data['name']}")
            else:
                existing_count += 1
                print(f"  [SKIP] Aplicação já existe (ID={existing_app.id}): {app_data['name']}")

        # Resetar a sequência do PostgreSQL para o próximo ID
        db.execute(text("SELECT setval(pg_get_serial_sequence('applications', 'id'), (SELECT COALESCE(MAX(id), 1) FROM applications))"))

        db.commit()

        print(f"\n{'='*60}")
        print(f"Seeder finalizado com sucesso!")
        print(f"Aplicações criadas: {created_count}")
        print(f"Aplicações já existentes: {existing_count}")
        print(f"Total de aplicações processadas: {len(applications_data)}")
        print(f"{'='*60}\n")

        # Mostrar resumo por categoria
        print("Resumo por Categoria:")
        apice_count = len([a for a in applications_data if a['category'] == 'APICE'])
        aise_count = len([a for a in applications_data if a['category'] == 'AISE'])
        web_count = len([a for a in applications_data if a['category'] == 'WEB'])
        oxy_count = len([a for a in applications_data if a['category'] == 'OXY'])
        portal_count = len([a for a in applications_data if a['category'] == 'Portal'])

        print(f"  - APICE: {apice_count} aplicações")
        print(f"  - AISE: {aise_count} aplicações")
        print(f"  - WEB: {web_count} aplicações")
        print(f"  - OXY: {oxy_count} aplicações")
        print(f"  - Portal: {portal_count} aplicações")
        print()

    except Exception as e:
        db.rollback()
        print(f"\n[ERRO] Erro ao executar seeder: {str(e)}\n")
        raise
    finally:
        db.close()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("SEEDER: Aplicações/Módulos")
    print("="*60 + "\n")
    seed_applications()
