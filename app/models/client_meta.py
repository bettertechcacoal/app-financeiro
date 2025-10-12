# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class ClientMeta(Base):
    """Modelo de metadados do cliente (padrão WordPress)"""
    __tablename__ = 'client_meta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    meta_key = Column(String(255), nullable=False)
    meta_value = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamento com Client
    client = relationship('Client', backref='meta_data')

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'meta_key': self.meta_key,
            'meta_value': self.meta_value,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
