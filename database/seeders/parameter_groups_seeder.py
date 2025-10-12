# -*- coding: utf-8 -*-
"""
Seeder para popular o banco de dados com grupos de parâmetros
"""
import sys
import os

# Adicionar o diretorio raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import SessionLocal
from app.models.parameter_group import ParameterGroup


def seed_parameter_groups():
    """Popula o banco com grupos de parâmetros"""

    db = SessionLocal()

    try:
        print("\n[SEEDER] Criando grupos de parâmetros...")

        # Grupos padrão do sistema
        groups_data = [
            {
                'name': 'Integrações',
                'description': 'Configurações de integrações com sistemas externos',
                'icon': 'fa-plug',
                'order': 1
            },
            {
                'name': 'E-mail',
                'description': 'Configurações de envio de e-mails',
                'icon': 'fa-envelope',
                'order': 2
            },
            {
                'name': 'Sistema',
                'description': 'Configurações gerais do sistema',
                'icon': 'fa-cog',
                'order': 3
            },
            {
                'name': 'Viagens',
                'description': 'Configurações do módulo de viagens',
                'icon': 'fa-plane-departure',
                'order': 4
            }
        ]

        created_count = 0
        existing_count = 0

        for group_data in groups_data:
            # Verifica se o grupo já existe
            existing_group = db.query(ParameterGroup).filter_by(
                name=group_data['name']
            ).first()

            if not existing_group:
                # Criar novo grupo
                group = ParameterGroup(**group_data)
                db.add(group)
                created_count += 1
                print(f"  [OK] Grupo criado: {group_data['name']}")
            else:
                # Atualizar informações do grupo
                existing_group.description = group_data['description']
                existing_group.icon = group_data['icon']
                existing_group.order = group_data['order']
                existing_count += 1
                print(f"  [OK] Grupo atualizado: {group_data['name']}")

        db.commit()

        print(f"\n{'='*60}")
        print(f"Seeder finalizado com sucesso!")
        print(f"Grupos criados: {created_count}")
        print(f"Grupos atualizados: {existing_count}")
        print(f"Total de grupos: {len(groups_data)}")
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
    print("SEEDER: Grupos de Parâmetros")
    print("="*60 + "\n")
    seed_parameter_groups()
