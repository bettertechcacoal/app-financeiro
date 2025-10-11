# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class State(Base):
    """Modelo de Estado - padrão Laravel"""
    __tablename__ = 'states'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    uf = Column(String(2), unique=True, nullable=False, index=True)
    ibge_code = Column(String(2), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamento com cidades
    cities = relationship('City', back_populates='state', cascade='all, delete-orphan')

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'uf': self.uf,
            'ibge_code': self.ibge_code,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
