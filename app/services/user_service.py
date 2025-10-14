# -*- coding: utf-8 -*-
from app.models.database import SessionLocal
from app.models.user import User


class UserService:
    """Serviço para gerenciamento de usuários"""

    def get_all_users(self):
        """Retorna todos os usuários"""
        db = SessionLocal()
        try:
            users = db.query(User).order_by(User.name).all()
            return [user.to_dict() for user in users]
        finally:
            db.close()

    def get_user_by_id(self, user_id):
        """Busca um usuário pelo ID"""
        db = SessionLocal()
        try:
            user = db.query(User).filter_by(id=user_id).first()
            if not user:
                return None
            return user.to_dict()
        finally:
            db.close()

    def get_user_with_groups(self, user_id):
        """Busca um usuário pelo ID com seus grupos"""
        db = SessionLocal()
        try:
            user = db.query(User).filter_by(id=user_id).first()
            if not user:
                return None

            # Buscar grupos do usuário
            from app.models.user_group import user_groups as user_groups_table
            from app.models.group import Group

            user_groups = db.query(Group).join(
                user_groups_table, user_groups_table.c.group_id == Group.id
            ).filter(
                user_groups_table.c.user_id == user.id
            ).all()

            # Converter para dict
            user_data = user.to_dict()
            user_data['groups'] = [group.to_dict() for group in user_groups]

            return user_data
        finally:
            db.close()

    def create_user(self, user_data):
        """Cria um novo usuário"""
        db = SessionLocal()
        try:
            user = User(
                name=user_data.get('name'),
                email=user_data.get('email'),
                phone=user_data.get('phone'),
                avatar=user_data.get('avatar'),
                is_active=user_data.get('is_active', True)
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return user.to_dict()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def update_user(self, user_id, user_data):
        """Atualiza um usuário"""
        db = SessionLocal()
        try:
            user = db.query(User).filter_by(id=user_id).first()
            if not user:
                return None

            user.name = user_data.get('name', user.name)
            user.email = user_data.get('email', user.email)
            user.phone = user_data.get('phone', user.phone)
            user.avatar = user_data.get('avatar', user.avatar)
            user.is_active = user_data.get('is_active', user.is_active)

            db.commit()
            db.refresh(user)
            return user.to_dict()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def delete_user(self, user_id):
        """Remove um usuário"""
        db = SessionLocal()
        try:
            user = db.query(User).filter_by(id=user_id).first()
            if not user:
                return False

            db.delete(user)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()


# Instância singleton do serviço
user_service = UserService()
