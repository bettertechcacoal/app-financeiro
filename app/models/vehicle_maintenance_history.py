# -*- coding: utf-8 -*-
"""
Model: VehicleMaintenanceHistory
Representa histórico de manutenções realizadas
"""

from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class VehicleMaintenanceHistory(Base):
    """Model para histórico de manutenções"""
    __tablename__ = 'vehicle_maintenance_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id', ondelete='CASCADE'), nullable=False, comment='ID do veículo')
    type_id = Column(Integer, ForeignKey('maintenance_types.id', ondelete='CASCADE'), nullable=False, comment='ID do tipo de manutenção')
    description = Column(Text, nullable=True, comment='Detalhes da manutenção')
    km_performed = Column(Integer, nullable=False, comment='KM quando foi realizada')
    cost = Column(Numeric(10, 2), nullable=True, comment='Custo da manutenção')
    performed_at = Column(DateTime, nullable=False, comment='Data da manutenção')
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment='Data de criação')

    # Relationships
    vehicle = relationship('Vehicle', back_populates='maintenance_history')
    maintenance_type = relationship('MaintenanceType', back_populates='maintenance_history')

    def __repr__(self):
        return f"<VehicleMaintenanceHistory vehicle_id={self.vehicle_id} type_id={self.type_id}>"

    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'type_id': self.type_id,
            'description': self.description,
            'km_performed': self.km_performed,
            'cost': float(self.cost) if self.cost else None,
            'performed_at': self.performed_at.isoformat() if self.performed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
