# -*- coding: utf-8 -*-
"""
Model: VehicleIssue
Representa problemas reportados em veículos
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class VehicleIssue(Base):
    """Model para problemas de veículos"""
    __tablename__ = 'vehicle_issues'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id', ondelete='CASCADE'), nullable=False, comment='ID do veículo')
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True, comment='ID do usuário que reportou')
    description = Column(Text, nullable=False, comment='Descrição do problema')
    status = Column(String(20), nullable=False, default='pendente', comment='Status: pendente, resolvido')
    resolved_at = Column(DateTime, nullable=True, comment='Data de resolução')
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment='Data de criação')

    # Relationships
    vehicle = relationship('Vehicle', back_populates='issues')
    user = relationship('User', foreign_keys=[user_id])

    def __repr__(self):
        return f"<VehicleIssue vehicle_id={self.vehicle_id} status={self.status}>"

    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'user_id': self.user_id,
            'description': self.description,
            'status': self.status,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
