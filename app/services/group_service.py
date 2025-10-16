# -*- coding: utf-8 -*-
from app.models.database import SessionLocal
from app.models.group import Group


class GroupService:
    """Serviço para gerenciamento de grupos"""

    def get_all_groups(self):
        """Retorna todos os grupos ativos"""
        db = SessionLocal()
        try:
            groups = db.query(Group).filter_by(is_active=True).order_by(Group.name).all()
            return [group.to_dict() for group in groups]
        finally:
            db.close()

    def get_group_by_id(self, group_id):
        """Busca um grupo pelo ID"""
        db = SessionLocal()
        try:
            group = db.query(Group).filter_by(id=group_id, is_active=True).first()
            if not group:
                return None
            return group.to_dict()
        finally:
            db.close()


# Instância singleton do serviço
group_service = GroupService()
