# -*- coding: utf-8 -*-
"""
Seeder para popular o banco de dados com grupos
"""
import sys
import os
import json

# Adicionar o diretorio raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import SessionLocal
from app.models.group import Group


def seed_groups():
    """Popula o banco com grupos padrao"""

    db = SessionLocal()

    try:
        # Definir grupos padrao
        groups_data = [
            {
                'name': 'Administradores',
                'slug': 'administradores',
                'description': 'Acesso total ao sistema',
                'color': '#dc2626',  # Vermelho
                'icon': 'fa-shield-alt',
                'hierarchy_level': 1,
                'permissions': json.dumps({
                    'users': {'create': True, 'read': True, 'update': True, 'delete': True},
                    'travels': {'create': True, 'read': True, 'update': True, 'delete': True, 'approve': True},
                    'clients': {'create': True, 'read': True, 'update': True, 'delete': True},
                    'tickets': {'create': True, 'read': True, 'update': True, 'delete': True},
                    'reports': {'read': True, 'export': True}
                })
            },
            {
                'name': 'Gestores',
                'slug': 'gestores',
                'description': 'Gerenciamento de equipes e aprovacao de viagens',
                'color': '#2563eb',  # Azul
                'icon': 'fa-user-tie',
                'hierarchy_level': 2,
                'permissions': json.dumps({
                    'users': {'create': False, 'read': True, 'update': False, 'delete': False},
                    'travels': {'create': True, 'read': True, 'update': True, 'delete': False, 'approve': True},
                    'clients': {'create': True, 'read': True, 'update': True, 'delete': False},
                    'tickets': {'create': True, 'read': True, 'update': True, 'delete': False},
                    'reports': {'read': True, 'export': True}
                })
            },
            {
                'name': 'Colaboradores',
                'slug': 'colaboradores',
                'description': 'Usuarios padrao do sistema',
                'color': '#16a34a',  # Verde
                'icon': 'fa-users',
                'hierarchy_level': 3,
                'permissions': json.dumps({
                    'users': {'create': False, 'read': False, 'update': False, 'delete': False},
                    'travels': {'create': True, 'read': True, 'update': True, 'delete': False, 'approve': False},
                    'clients': {'create': False, 'read': True, 'update': False, 'delete': False},
                    'tickets': {'create': True, 'read': True, 'update': False, 'delete': False},
                    'reports': {'read': True, 'export': False}
                })
            },
            {
                'name': 'Visitantes',
                'slug': 'visitantes',
                'description': 'Acesso somente leitura',
                'color': '#9ca3af',  # Cinza
                'icon': 'fa-eye',
                'hierarchy_level': 4,
                'permissions': json.dumps({
                    'users': {'create': False, 'read': False, 'update': False, 'delete': False},
                    'travels': {'create': False, 'read': True, 'update': False, 'delete': False, 'approve': False},
                    'clients': {'create': False, 'read': True, 'update': False, 'delete': False},
                    'tickets': {'create': False, 'read': True, 'update': False, 'delete': False},
                    'reports': {'read': True, 'export': False}
                })
            }
        ]

        created_count = 0
        existing_count = 0

        for group_data in groups_data:
            # Verifica se o grupo ja existe
            existing_group = db.query(Group).filter_by(slug=group_data['slug']).first()

            if not existing_group:
                group = Group(
                    name=group_data['name'],
                    slug=group_data['slug'],
                    description=group_data['description'],
                    color=group_data['color'],
                    icon=group_data['icon'],
                    hierarchy_level=group_data['hierarchy_level'],
                    permissions=group_data['permissions'],
                    is_active=True
                )
                db.add(group)
                created_count += 1
                print(f"  [OK] Grupo criado: {group_data['name']}")
            else:
                existing_count += 1
                print(f"  [OK] Grupo ja existe: {group_data['name']}")

        db.commit()

        print(f"\n{'='*60}")
        print(f"Seeder finalizado com sucesso!")
        print(f"Grupos criados: {created_count}")
        print(f"Grupos ja existentes: {existing_count}")
        print(f"Total de grupos: {len(groups_data)}")
        print(f"{'='*60}\n")

    except Exception as e:
        db.rollback()
        print(f"\n[ERRO] Erro ao executar seeder: {str(e)}\n")
        raise
    finally:
        db.close()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("SEEDER: Grupos")
    print("="*60 + "\n")
    seed_groups()
