# -*- coding: utf-8 -*-
"""
Seeder para popular o banco de dados com grupos
"""
import sys
from config import ROOT_DIR

# Adicionar o diretorio raiz ao path
sys.path.insert(0, ROOT_DIR)

from app.models.database import SessionLocal
from app.models.group import Group
from sqlalchemy import text


def seed_groups():
    """Popula o banco com grupos padrao"""

    db = SessionLocal()

    try:
        # Definir grupos padrao com IDs fixos
        groups_data = [
            {
                'id': 1,
                'name': 'Administradores',
                'slug': 'administradores',
                'description': 'Acesso total ao sistema',
                'color': '#dc2626',  # Vermelho
                'icon': 'fa-shield-alt'
            }
        ]

        created_count = 0
        existing_count = 0

        for group_data in groups_data:
            # Verifica se o grupo ja existe
            existing_group = db.query(Group).filter_by(id=group_data['id']).first()

            if not existing_group:
                # Inserir com ID fixo usando SQL direto
                db.execute(
                    text("""
                        INSERT INTO groups (id, name, slug, description, color, icon, is_active, created_at, updated_at)
                        VALUES (:id, :name, :slug, :description, :color, :icon, :is_active, NOW(), NOW())
                    """),
                    {
                        "id": group_data['id'],
                        "name": group_data['name'],
                        "slug": group_data['slug'],
                        "description": group_data['description'],
                        "color": group_data['color'],
                        "icon": group_data['icon'],
                        "is_active": True
                    }
                )
                created_count += 1
                print(f"  [OK] Grupo criado: {group_data['name']} (ID: {group_data['id']})")
            else:
                existing_count += 1
                print(f"  [OK] Grupo ja existe: {group_data['name']} (ID: {group_data['id']})")

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
