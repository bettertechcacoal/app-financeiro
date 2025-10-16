# -*- coding: utf-8 -*-
"""
Model: MaintenanceType
Representa tipos de manutenção disponíveis
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class MaintenanceType(Base):
    """Model para tipos de manutenção"""
    __tablename__ = 'maintenance_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True, comment='Nome do tipo de manutenção')
    description = Column(Text, nullable=True, comment='Descrição detalhada')
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment='Data de criação')

    # Relationships
    maintenance_history = relationship('VehicleMaintenanceHistory', back_populates='maintenance_type')
    maintenance_configs = relationship('VehicleMaintenanceConfig', back_populates='maintenance_type')

    def __repr__(self):
        return f"<MaintenanceType {self.name}>"

    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
