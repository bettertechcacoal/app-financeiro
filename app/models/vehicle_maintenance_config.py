# -*- coding: utf-8 -*-
"""
Model: VehicleMaintenanceConfig
Representa configurações de manutenção programada de veículos
"""

from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class VehicleMaintenanceConfig(Base):
    """Model para configurações de manutenção"""
    __tablename__ = 'vehicle_maintenance_configs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id', ondelete='CASCADE'), nullable=False, comment='ID do veículo')
    maintenance_type_id = Column(Integer, ForeignKey('maintenance_types.id', ondelete='CASCADE'), nullable=False, comment='ID do tipo de manutenção')
    km_interval = Column(Integer, nullable=False, comment='Intervalo em KM entre manutenções')
    is_active = Column(Boolean, nullable=False, default=True, comment='Configuração ativa')
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment='Data de criação')
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment='Data de atualização')

    # Relationships
    vehicle = relationship('Vehicle', back_populates='maintenance_configs')
    maintenance_type = relationship('MaintenanceType', back_populates='maintenance_configs')

    def __repr__(self):
        return f"<VehicleMaintenanceConfig vehicle_id={self.vehicle_id} type_id={self.maintenance_type_id}>"

    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'maintenance_type_id': self.maintenance_type_id,
            'maintenance_type_name': self.maintenance_type.name if self.maintenance_type else None,
            'km_interval': self.km_interval,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
