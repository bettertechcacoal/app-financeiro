# -*- coding: utf-8 -*-
"""
Seeder para popular o banco de dados com usuarios de teste
"""
import sys
import os
from datetime import datetime

# Adicionar o diretorio raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import SessionLocal
from app.models.user import User
from app.models.group import Group
from sqlalchemy import text


def seed_users():
    """Popula o banco com usuarios de teste"""

    db = SessionLocal()

    try:
        # Buscar grupos
        admin_group = db.query(Group).filter_by(slug='administradores').first()
        gestor_group = db.query(Group).filter_by(slug='gestores').first()
        colaborador_group = db.query(Group).filter_by(slug='colaboradores').first()

        if not admin_group or not gestor_group or not colaborador_group:
            print("\n[ERRO] Grupos nao encontrados!")
            print("Execute primeiro: python database/seeders/groups_seeder.py")
            return

        # Definir usuarios de teste
        users_data = [
            # Usuario original
            {
                'name': 'Usuario Demo',
                'email': 'demo@demo.com',
                'phone': '(69) 99999-0000',
                'group_id': admin_group.id,
                'email_verified_at': datetime.now()
            },
            # 10 novos usuarios ficticios
            {
                'name': 'Maria Silva',
                'email': 'maria.silva@empresa.com',
                'phone': '(69) 98765-4321',
                'group_id': admin_group.id,
                'email_verified_at': datetime.now()
            },
            {
                'name': 'João Santos',
                'email': 'joao.santos@empresa.com',
                'phone': '(69) 98765-4322',
                'group_id': gestor_group.id,
                'email_verified_at': datetime.now()
            },
            {
                'name': 'Ana Costa',
                'email': 'ana.costa@empresa.com',
                'phone': '(69) 98765-4323',
                'group_id': gestor_group.id,
                'email_verified_at': datetime.now()
            },
            {
                'name': 'Pedro Oliveira',
                'email': 'pedro.oliveira@empresa.com',
                'phone': '(69) 98765-4324',
                'group_id': colaborador_group.id,
                'email_verified_at': datetime.now()
            },
            {
                'name': 'Carla Souza',
                'email': 'carla.souza@empresa.com',
                'phone': '(69) 98765-4325',
                'group_id': colaborador_group.id,
                'email_verified_at': datetime.now()
            },
            {
                'name': 'Ricardo Ferreira',
                'email': 'ricardo.ferreira@empresa.com',
                'phone': '(69) 98765-4326',
                'group_id': colaborador_group.id,
                'email_verified_at': datetime.now()
            },
            {
                'name': 'Juliana Alves',
                'email': 'juliana.alves@empresa.com',
                'phone': '(69) 98765-4327',
                'group_id': gestor_group.id,
                'email_verified_at': datetime.now()
            },
            {
                'name': 'Marcos Lima',
                'email': 'marcos.lima@empresa.com',
                'phone': '(69) 98765-4328',
                'group_id': colaborador_group.id,
                'email_verified_at': datetime.now()
            },
            {
                'name': 'Fernanda Rocha',
                'email': 'fernanda.rocha@empresa.com',
                'phone': '(69) 98765-4329',
                'group_id': colaborador_group.id,
                'email_verified_at': datetime.now()
            },
            {
                'name': 'Bruno Martins',
                'email': 'bruno.martins@empresa.com',
                'phone': '(69) 98765-4330',
                'group_id': gestor_group.id,
                'email_verified_at': datetime.now()
            },
            {
                'name': 'Patricia Mendes',
                'email': 'patricia.mendes@empresa.com',
                'phone': '(69) 98765-4331',
                'group_id': colaborador_group.id,
                'email_verified_at': datetime.now()
            }
        ]

        created_count = 0
        existing_count = 0

        for user_data in users_data:
            # Verifica se o usuario ja existe
            existing_user = db.query(User).filter_by(email=user_data['email']).first()

            if not existing_user:
                # Criar usuario
                user = User(
                    name=user_data['name'],
                    email=user_data['email'],
                    phone=user_data['phone'],
                    is_active=True,
                    email_verified_at=user_data['email_verified_at']
                )
                db.add(user)
                db.flush()  # Para obter o ID do usuario

                # Vincular ao grupo atraves da tabela pivot
                db.execute(
                    text("INSERT INTO user_groups (user_id, group_id) VALUES (:user_id, :group_id)"),
                    {"user_id": user.id, "group_id": user_data['group_id']}
                )

                created_count += 1
                print(f"  [OK] Usuario criado: {user_data['name']} ({user_data['email']})")
            else:
                existing_count += 1
                print(f"  [OK] Usuario ja existe: {user_data['name']}")

        db.commit()

        print(f"\n{'='*60}")
        print(f"Seeder finalizado com sucesso!")
        print(f"Usuarios criados: {created_count}")
        print(f"Usuarios ja existentes: {existing_count}")
        print(f"Total de usuarios: {len(users_data)}")
        print(f"{'='*60}\n")

        # Mostrar resumo
        print("Resumo dos usuarios:")
        print(f"  Administradores (2):")
        print(f"    - Usuario Demo (demo@demo.com)")
        print(f"    - Maria Silva (maria.silva@empresa.com)")
        print(f"  Gestores (4):")
        print(f"    - João Santos (joao.santos@empresa.com)")
        print(f"    - Ana Costa (ana.costa@empresa.com)")
        print(f"    - Juliana Alves (juliana.alves@empresa.com)")
        print(f"    - Bruno Martins (bruno.martins@empresa.com)")
        print(f"  Colaboradores (5):")
        print(f"    - Pedro Oliveira (pedro.oliveira@empresa.com)")
        print(f"    - Carla Souza (carla.souza@empresa.com)")
        print(f"    - Ricardo Ferreira (ricardo.ferreira@empresa.com)")
        print(f"    - Marcos Lima (marcos.lima@empresa.com)")
        print(f"    - Fernanda Rocha (fernanda.rocha@empresa.com)")
        print(f"    - Patricia Mendes (patricia.mendes@empresa.com)")
        print()

    except Exception as e:
        db.rollback()
        print(f"\n[ERRO] Erro ao executar seeder: {str(e)}\n")
        raise
    finally:
        db.close()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("SEEDER: Usuarios de Teste")
    print("="*60 + "\n")
    seed_users()
