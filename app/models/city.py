# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class City(Base):
    """Modelo de Cidade - padrão Laravel"""
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    ibge_code = Column(String(7), unique=True, nullable=False, index=True)

    # Relacionamento com estado
    state_id = Column(Integer, ForeignKey('states.id'), nullable=False)
    state = relationship('State', back_populates='cities')

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamento com viagens
    travels = relationship('Travel', back_populates='city', cascade='all, delete-orphan')

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'ibge_code': self.ibge_code,
            'state_id': self.state_id,
            'state': self.state.to_dict() if self.state else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
