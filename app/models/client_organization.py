# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.models.database import Base


class ClientOrganization(Base):
    """Tabela de relacionamento entre Clientes e Organizações (muitos-para-muitos)"""
    __tablename__ = 'client_organizations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    organization_id = Column(String(50), ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'organization_id': self.organization_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
