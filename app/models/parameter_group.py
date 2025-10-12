# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class ParameterGroup(Base):
    """Modelo de Grupos de Parâmetros"""
    __tablename__ = 'parameter_groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)  # Nome do grupo (ex: Integrações, E-mail, Sistema)
    description = Column(String(255), nullable=False)  # Descrição do grupo
    icon = Column(String(50))  # Ícone Font Awesome (ex: fa-plug, fa-envelope)
    order = Column(Integer, default=0, nullable=False)  # Ordem de exibição

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamento com parâmetros
    parameters = relationship('Parameter', back_populates='group', cascade='all, delete-orphan')

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'order': self.order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
