# -*- coding: utf-8 -*-
"""
Seeder para popular o banco de dados com associações cliente-aplicação
Usa IDs fixos para cliente e aplicação
"""
import sys
import os

# Adicionar o diretorio raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import SessionLocal
from app.models.client_application import ClientApplication


def seed_client_applications():
    """Popula o banco com associações cliente-aplicação usando IDs fixos"""

    db = SessionLocal()

    try:
        # Mapeamento: client_id -> [lista de application_ids]
        # IDs dos Clientes (conforme ordem no clients_seeder.py):
        # 1: Prefeitura Municipal de Alta Floresta d'Oeste
        # 2: Câmara Municipal de Alta Floresta d'Oeste
        # 3: SAAE - Alta Floresta d'Oeste
        # 4: Prefeitura Municipal de Cacoal
        # 5: Câmara Municipal de Cacoal
        # 6: Prefeitura Municipal de Castanheiras
        # 7: Câmara Municipal de Castanheiras
        # 8: Instituto de Previdência de Castanheiras
        # 9: Prefeitura Municipal de Ministro Andreazza
        # 10: Câmara Municipal de Ministro Andreazza
        # 11: Prefeitura Municipal de Nova Brasilândia d'Oeste
        # 12: Câmara Municipal de Nova Brasilândia d'Oeste
        # 13: SAAE - Nova Brasilândia d'Oeste
        # 14: Prefeitura Municipal de Rio Crespo
        # 15: Câmara Municipal de Rio Crespo
        # 16: Prefeitura Municipal de Rolim de Moura
        # 17: Câmara Municipal de Rolim de Moura
        # 18: Instituto de Previdência de Rolim de Moura
        # 19: Prefeitura Municipal de São Felipe d'Oeste
        # 20: Câmara Municipal de São Felipe d'Oeste
        # 21: Prefeitura Municipal de São Miguel do Guaporé
        # 22: Câmara Municipal de São Miguel do Guaporé
        # 23: Prefeitura Municipal de Seringueiras
        # 24: Câmara Municipal de Seringueiras
        # 25: Fundo de Previdência de Seringueiras
        # 26: Prefeitura Municipal de Urupá
        # 27: Câmara Municipal de Urupá
        # 28: Prefeitura Municipal de Vale do Anari
        # 29: Câmara Municipal de Vale do Anari
        # 30: Prefeitura Municipal de Vilhena
        # 31: Câmara Municipal de Vilhena
        # 32: SAAE - Vilhena
        # 33: Instituto de Previdência de Vilhena

        # IDs das Aplicações (conforme ordem no applications_seeder.py):
        # 1: APICE - Orçamento
        # 2: APICE- Contabilidade
        # 3: APICE-Protocolo
        # 4: APICE-Patrimonio
        # 5: APICE-Frotas
        # 6: APICE - SigEloAM
        # 7: APICE-Tesouraria
        # 8: APICE- Almoxarifado
        # 9: APICE- Compras e Licitações
        # 10: AISE- Controle de Obras
        # 11: AISE-  Folha de Pagamento RH
        # 12: AISE -Tributos
        # 13: Portal Transparencia
        # 14: WEB - Issqn
        # 15: WEB - Tributos
        # 16: WEB - Cemitério
        # 17: WEB - Alvará Online
        # 18: WEB- Portal RH
        # 19: OXY- Cidadão APP- Mobile
        # 20: OXY - Custos
        # 21: OXY - Cidadão ITBI Online
        # 22: OXY Folha de Pagamento

        client_applications_map = {
            # 1: Prefeitura Municipal de Alta Floresta d'Oeste
            1: [1, 2, 3, 4, 5, 6, 7, 8, 10, 13, 15, 16, 17, 18, 19, 11, 9, 12],

            # 4: Prefeitura Municipal de Cacoal
            4: [1, 2, 3, 4, 5, 6, 7, 8, 10, 13, 15, 16, 17, 18, 21, 19, 11, 9, 12],

            # 6: Prefeitura Municipal de Castanheiras
            6: [1, 2, 3, 4, 5, 6, 7, 8, 10, 14, 13, 15, 17, 18, 11, 9, 12],

            # 9: Prefeitura Municipal de Ministro Andreazza
            9: [1, 2, 3, 4, 5, 6, 7, 8, 10, 13, 15, 18, 19, 11, 9, 12],

            # 11: Prefeitura Municipal de Nova Brasilândia d'Oeste
            11: [1, 2, 4, 5, 6, 7, 8, 10, 14, 13, 15, 16, 17, 18, 19, 11, 9, 12],

            # 14: Prefeitura Municipal de Rio Crespo
            14: [1, 2, 3, 4, 5, 6, 7, 8, 10, 14, 13, 15, 17, 18, 21, 11, 9, 12],

            # 16: Prefeitura Municipal de Rolim de Moura
            16: [16, 17, 12],

            # 19: Prefeitura Municipal de São Felipe d'Oeste
            19: [1, 2, 3, 4, 5, 6, 7, 8, 10, 14, 13, 15, 18, 11, 9, 12],

            # 21: Prefeitura Municipal de São Miguel do Guaporé
            21: [1, 2, 3, 4, 5, 6, 7, 8, 10, 14, 13, 15, 18, 11, 9, 12],

            # 23: Prefeitura Municipal de Seringueiras
            23: [1, 2, 3, 4, 5, 6, 7, 8, 10, 14, 13, 15, 16, 18, 19, 11, 9, 12],

            # 26: Prefeitura Municipal de Urupá
            26: [16, 17, 12],

            # 28: Prefeitura Municipal de Vale do Anari
            28: [1, 2, 3, 4, 5, 6, 7, 8, 10, 14, 13, 15, 16, 17, 18, 19, 11, 9, 12],

            # 30: Prefeitura Municipal de Vilhena
            30: [16, 17, 12],
        }

        created_count = 0
        skipped_count = 0

        for client_id, application_ids in client_applications_map.items():
            for application_id in application_ids:
                # Verificar se associação já existe
                existing = db.query(ClientApplication).filter_by(
                    client_id=client_id,
                    application_id=application_id
                ).first()

                if existing:
                    skipped_count += 1
                    continue

                # Criar associação
                client_app = ClientApplication(
                    client_id=client_id,
                    application_id=application_id,
                    is_active=True
                )
                db.add(client_app)
                created_count += 1

            print(f"  [OK] Cliente ID={client_id} associado com {len(application_ids)} aplicações")

        db.commit()

        print(f"\n{'='*60}")
        print(f"Seeder finalizado com sucesso!")
        print(f"Associações criadas: {created_count}")
        print(f"Associações já existentes: {skipped_count}")
        print(f"Clientes processados: {len(client_applications_map)}")
        print(f"{'='*60}\n")

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
    print("SEEDER: Associações Cliente-Aplicação")
    print("="*60 + "\n")
    seed_client_applications()
