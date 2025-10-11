# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class Group(Base):
    """Modelo de Grupo - padrao Laravel"""
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    color = Column(String(20), default='#3b82f6')  # Azul padrao
    icon = Column(String(50), default='fa-users')
    permissions = Column(Text)  # JSON serializado
    hierarchy_level = Column(Integer, default=99)  # 1 = mais alto, 99 = mais baixo
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


    def to_dict(self):
        """Converte o modelo para dicionario"""
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'color': self.color,
            'icon': self.icon,
            'permissions': self.permissions,
            'hierarchy_level': self.hierarchy_level,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
