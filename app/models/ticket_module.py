# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.models.database import Base


class TicketModule(Base):
    """Modelo de Módulo de Ticket"""
    __tablename__ = 'tickets_modules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(500))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
