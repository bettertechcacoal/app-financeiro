# -*- coding: utf-8 -*-
"""
Seeder de Grupos
Popula a tabela de grupos com perfis de acesso do sistema
"""
import sys
from config import ROOT_DIR

sys.path.insert(0, ROOT_DIR)

from app.models.database import SessionLocal
from app.models.group import Group
from sqlalchemy import text


def seed_groups():
    """Cria grupos de acesso padrão com IDs fixos"""
    db = SessionLocal()

    try:
        # Grupos padrão do sistema
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

        for group_data in groups_data:
            existing_group = db.query(Group).filter_by(id=group_data['id']).first()

            if not existing_group:
                # Criar grupo com ID fixo
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

        # Ajustar sequência de auto incremento do PostgreSQL
        db.execute(text("SELECT setval(pg_get_serial_sequence('groups', 'id'), (SELECT COALESCE(MAX(id), 1) FROM groups))"))
        db.commit()

        print("[SUCCESS] Seeder de grupos executado com sucesso")

    except Exception as e:
        db.rollback()
        print(f"[ERRO] {type(e).__name__}: {str(e).split(chr(10))[0]}")
    finally:
        db.close()


if __name__ == '__main__':
    seed_groups()
