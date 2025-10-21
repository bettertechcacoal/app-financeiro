# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class User(Base):
    """Modelo de Usuario do sistema - padrao Laravel"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20))
    avatar = Column(String(255))

    # Status e controle
    active = Column(Boolean, default=True, nullable=False)
    sid_uuid = Column(String(36), unique=True, nullable=True, index=True)
    email_verified_at = Column(DateTime(timezone=True))
    last_login_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamento com viagens (como motorista/viajante)
    travels = relationship('Travel', foreign_keys='Travel.driver_user_id', back_populates='driver_user')

    # Relacionamento many-to-many com Group através de user_groups
    groups = relationship('Group', secondary='user_groups', backref='users')

    def to_dict(self):
        """Converte o modelo para dicionario"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'avatar': self.avatar,
            'active': self.active,
            'sid_uuid': self.sid_uuid,
            'email_verified_at': self.email_verified_at.isoformat() if self.email_verified_at else None,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def has_permission(self, permission_slug):
        """Verifica se o usuário possui uma permissão específica através de seus grupos"""
        for group in self.groups:
            if group.has_permission(permission_slug):
                return True
        return False

    def has_any_permission(self, permission_slugs):
        """Verifica se o usuário possui pelo menos uma das permissões especificadas"""
        return any(self.has_permission(slug) for slug in permission_slugs)

    def has_all_permissions(self, permission_slugs):
        """Verifica se o usuário possui todas as permissões especificadas"""
        return all(self.has_permission(slug) for slug in permission_slugs)

    def get_all_permissions(self):
        """Retorna todas as permissões do usuário (de todos os grupos)"""
        permissions = set()
        for group in self.groups:
            permissions.update(group.get_permissions_slugs())
        return list(permissions)

    def is_in_group(self, group_slug):
        """Verifica se o usuário pertence a um grupo específico"""
        return any(group.slug == group_slug for group in self.groups)
