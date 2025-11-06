# -*- coding: utf-8 -*-
"""
Seeder de Usuários
Popula a tabela de usuários com registros iniciais do sistema
"""
import sys
from datetime import datetime
from config import ROOT_DIR

sys.path.insert(0, ROOT_DIR)

from app.models.database import SessionLocal
from app.models.user import User
from app.models.group import Group
from sqlalchemy import text


def seed_users():
    """Cria usuários da equipe BetterTech"""
    db = SessionLocal()

    try:
        # Usuário administrador com ID fixo
        admin_user = {
            "id": 1,
            "sid_uuid": 'e7f8a9b0-c1d2-4e7f-4a5b-6c7d8e9f0a1b',
            "name": 'Renan Silva',
            "email": 'renan@bettertech.com.br',
            "phone": '(69) 99999-0000'
        }

        # Verificar se admin já existe
        existing_admin = db.query(User).filter_by(email=admin_user['email']).first()

        if not existing_admin:
            # Criar usuário administrador com ID fixo
            db.execute(
                text("""
                    INSERT INTO users (id, sid_uuid, name, email, phone, active, email_verified_at, created_at, updated_at)
                    VALUES (:id, :sid_uuid, :name, :email, :phone, :active, :email_verified_at, NOW(), NOW())
                """),
                {
                    "id": admin_user['id'],
                    "sid_uuid": admin_user['sid_uuid'],
                    "name": admin_user['name'],
                    "email": admin_user['email'],
                    "phone": admin_user['phone'],
                    "active": True,
                    "email_verified_at": datetime.now()
                }
            )

            # Vincular ao grupo de administradores
            db.execute(
                text("INSERT INTO user_groups (user_id, group_id) VALUES (:user_id, :group_id)"),
                {"user_id": admin_user['id'], "group_id": 1}
            )

        # Demais usuários da equipe (ordem alfabética) com IDs fixos
        users = [
            {"id": 2, "sid_uuid": 'a1b2c3d4-e5f6-4a1b-8c9d-0e1f2a3b4c5d', "name": 'Alisson de Jesus', "email": 'alisson@bettertech.com.br', "phone": '(69) 99999-0001'},
            {"id": 3, "sid_uuid": 'b2c3d4e5-f6a7-4b2c-9d0e-1f2a3b4c5d6e', "name": 'Alyysson F. Armondes', "email": 'alyysson@bettertech.com.br', "phone": '(69) 99999-0002'},
            {"id": 4, "sid_uuid": 'c3d4e5f6-a7b8-4c3d-0e1f-2a3b4c5d6e7f', "name": 'Andre Poubel', "email": 'andre@bettertech.com.br', "phone": '(69) 99999-0003'},
            {"id": 5, "sid_uuid": 'd4e5f6a7-b8c9-4d4e-1f2a-3b4c5d6e7f8a', "name": 'Bianca', "email": 'bianca@bettertech.com.br', "phone": '(69) 99999-0004'},
            {"id": 6, "sid_uuid": 'e5f6a7b8-c9d0-4e5f-2a3b-4c5d6e7f8a9b', "name": 'Cezar Augusto dos Reis', "email": 'cezar@bettertech.com.br', "phone": '(69) 99999-0005'},
            {"id": 7, "sid_uuid": 'f6a7b8c9-d0e1-4f6a-3b4c-5d6e7f8a9b0c', "name": 'Cleiton', "email": 'cleiton@bettertech.com.br', "phone": '(69) 99999-0006'},
            {"id": 8, "sid_uuid": 'a7b8c9d0-e1f2-4a7b-4c5d-6e7f8a9b0c1d', "name": 'Diogo Antonio Ramos da Costa', "email": 'diogo@bettertech.com.br', "phone": '(69) 99999-0007'},
            {"id": 9, "sid_uuid": 'b8c9d0e1-f2a3-4b8c-5d6e-7f8a9b0c1d2e', "name": 'Eduardo Gabrio Sesana Apoluceno', "email": 'eduardo@bettertech.com.br', "phone": '(69) 99999-0008'},
            {"id": 10, "sid_uuid": 'c9d0e1f2-a3b4-4c9d-6e7f-8a9b0c1d2e3f', "name": 'Fabio Matte', "email": 'fabio@bettertech.com.br', "phone": '(69) 99999-0009'},
            {"id": 11, "sid_uuid": 'd0e1f2a3-b4c5-4d0e-7f8a-9b0c1d2e3f4a', "name": 'Gabriel Trevisan', "email": 'gabriel@bettertech.com.br', "phone": '(69) 99999-0010'},
            {"id": 12, "sid_uuid": 'e1f2a3b4-c5d6-4e1f-8a9b-0c1d2e3f4a5b', "name": 'Hugo Dorigo Dias', "email": 'hugo@bettertech.com.br', "phone": '(69) 99999-0011'},
            {"id": 13, "sid_uuid": 'f2a3b4c5-d6e7-4f2a-9b0c-1d2e3f4a5b6c', "name": 'Lucas Henrinque', "email": 'lucas@bettertech.com.br', "phone": '(69) 99999-0012'},
            {"id": 14, "sid_uuid": 'a3b4c5d6-e7f8-4a3b-0c1d-2e3f4a5b6c7d', "name": 'Luiz Paulo Trevisan', "email": 'luizpaulo@bettertech.com.br', "phone": '(69) 99999-0013'},
            {"id": 15, "sid_uuid": 'b4c5d6e7-f8a9-4b4c-1d2e-3f4a5b6c7d8e', "name": 'Rafael Ferreira Costa', "email": 'rafael@bettertech.com.br', "phone": '(69) 99999-0014'},
            {"id": 16, "sid_uuid": 'c5d6e7f8-a9b0-4c5d-2e3f-4a5b6c7d8e9f', "name": 'Raphael Kauan', "email": 'raphael.antunes@bettertech.com.br', "phone": '(69) 99999-0015'},
            {"id": 17, "sid_uuid": 'd6e7f8a9-b0c1-4d6e-3f4a-5b6c7d8e9f0a', "name": 'Reginaldo', "email": 'reginaldo@bettertech.com.br', "phone": '(69) 99999-0016'},
            {"id": 18, "sid_uuid": 'f8a9b0c1-d2e3-4f8a-5b6c-7d8e9f0a1b2c', "name": 'Rogerio Augusto Amaral', "email": 'rogerio@bettertech.com.br', "phone": '(69) 99999-0017'},
            {"id": 19, "sid_uuid": 'a9b0c1d2-e3f4-4a9b-6c7d-8e9f0a1b2c3d', "name": 'Ronildo Pauli da G. P.', "email": 'ronildopauli@bettertech.com.br', "phone": '(69) 99999-0018'},
            {"id": 20, "sid_uuid": 'b0c1d2e3-f4a5-4b0c-7d8e-9f0a1b2c3d4e', "name": 'Sidinei Flegler de Sousa', "email": 'sidinei@bettertech.com.br', "phone": '(69) 99999-0019'},
            {"id": 21, "sid_uuid": 'c1d2e3f4-a5b6-4c1d-8e9f-0a1b2c3d4e5f', "name": 'Victor Hugo Barbosa de Sena', "email": 'victor@bettertech.com.br', "phone": '(69) 99999-0020'},
        ]

        # Criar demais usuários sem vínculo ao grupo de administradores
        for user_data in users:
            existing_user = db.query(User).filter_by(email=user_data['email']).first()

            if not existing_user:
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

        # Ajustar sequência de auto incremento do PostgreSQL
        db.execute(text("SELECT setval(pg_get_serial_sequence('users', 'id'), (SELECT COALESCE(MAX(id), 1) FROM users))"))
        db.commit()

        print("[SUCCESS] Seeder de usuários executado com sucesso")

    except Exception as e:
        db.rollback()
        print(f"[ERRO] {type(e).__name__}: {str(e).split(chr(10))[0]}")
    finally:
        db.close()


if __name__ == '__main__':
    seed_users()
