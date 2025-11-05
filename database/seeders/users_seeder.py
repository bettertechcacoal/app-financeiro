# -*- coding: utf-8 -*-
"""
Seeder para popular o banco de dados com usuarios de teste
"""
import sys
from datetime import datetime
from config import ROOT_DIR

# Adicionar o diretorio raiz ao path
sys.path.insert(0, ROOT_DIR)

from app.models.database import SessionLocal
from app.models.user import User
from app.models.group import Group
from sqlalchemy import text


def seed_users():
    """Popula o banco com usuarios de teste"""

    db = SessionLocal()

    try:
        # ID fixo do grupo de administradores
        admin_group_id = 1

        # Lista de usuários para criar
        users = [
            {
                "id": 1,
                "sid_uuid": '019a0333-7cc7-7530-8c15-ca31ccd295d2',
                "name": 'Renan',
                "email": 'renan@bettertech.com.br',
                "phone": '(69) 99999-0000'
            },
            {
                "id": 2,
                "sid_uuid": '019a0333-8dd8-8641-9d26-db42dde3a6e3',
                "name": 'Lina Maria',
                "email": 'lina@bettertech.com.br',
                "phone": '(69) 99999-0001'
            },
            {
                "id": 3,
                "sid_uuid": '019a0333-9ee9-9752-ae37-ec53eef4b7f4',
                "name": 'Eduardo Gabrio',
                "email": 'eduardo@bettertech.com.br',
                "phone": '(69) 99999-0002'
            }
        ]

        for user_data in users:
            # Verifica se o usuario ja existe
            existing_user = db.query(User).filter_by(email=user_data['email']).first()

            if not existing_user:
                # Criar usuario com ID fixo
                db.execute(
                    text("""
                        INSERT INTO users (id, sid_uuid, name, email, phone, active, email_verified_at, created_at, updated_at)
                        VALUES (:id, :sid_uuid, :name, :email, :phone, :active, :email_verified_at, NOW(), NOW())
                    """),
                    {
                        "id": user_data['id'],
                        "sid_uuid": user_data['sid_uuid'],
                        "name": user_data['name'],
                        "email": user_data['email'],
                        "phone": user_data['phone'],
                        "active": True,
                        "email_verified_at": datetime.now()
                    }
                )

                # Vincular ao grupo de administradores (ID fixo = 1)
                db.execute(
                    text("INSERT INTO user_groups (user_id, group_id) VALUES (:user_id, :group_id)"),
                    {"user_id": user_data['id'], "group_id": admin_group_id}
                )

                print(f"  [OK] Usuario criado: {user_data['name']} (vinculado ao grupo Administradores - ID 1)")
            else:
                # Verifica se já está vinculado ao grupo de administradores
                existing_link = db.execute(
                    text("SELECT 1 FROM user_groups WHERE user_id = :user_id AND group_id = :group_id"),
                    {"user_id": user_data['id'], "group_id": admin_group_id}
                ).fetchone()

                if not existing_link:
                    # Vincular ao grupo de administradores
                    db.execute(
                        text("INSERT INTO user_groups (user_id, group_id) VALUES (:user_id, :group_id)"),
                        {"user_id": user_data['id'], "group_id": admin_group_id}
                    )
                    print(f"  [OK] Usuario ja existe: {user_data['name']} (vinculado ao grupo Administradores - ID 1)")
                else:
                    print(f"  [OK] Usuario ja existe: {user_data['name']} (ja vinculado ao grupo Administradores)")

        db.commit()

    except Exception as e:
        db.rollback()
        print(f"[ERRO] {type(e).__name__}: {str(e).split(chr(10))[0]}")
    finally:
        db.close()


if __name__ == '__main__':
    seed_users()
