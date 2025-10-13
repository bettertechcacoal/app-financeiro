# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class ClientApplication(Base):
    """Modelo de associação Cliente-Aplicação (N:N)"""
    __tablename__ = 'client_applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    application_id = Column(Integer, ForeignKey('applications.id', ondelete='CASCADE'), nullable=False)
    cod_elotech = Column(String(15), nullable=True)
    is_active = Column(Boolean, default=True, server_default='1', nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    client = relationship('Client', backref='client_applications')
    application = relationship('Application', backref='client_applications')

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'application_id': self.application_id,
            'cod_elotech': self.cod_elotech,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
