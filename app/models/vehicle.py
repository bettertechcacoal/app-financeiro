# -*- coding: utf-8 -*-
"""
Model: Vehicle
Representa um veículo da frota
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class Vehicle(Base):
    """Model para veículos da frota"""
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    plate = Column(String(10), nullable=False, unique=True, comment='Placa do veículo')
    model = Column(String(100), nullable=False, comment='Modelo do veículo')
    brand = Column(String(50), nullable=False, comment='Marca do veículo')
    year = Column(Integer, nullable=False, comment='Ano de fabricação')
    is_active = Column(Boolean, nullable=False, default=True, comment='Veículo ativo')
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment='Data de criação')
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment='Data de atualização')

    # Relationships
    km_logs = relationship('VehicleKmLog', back_populates='vehicle', cascade='all, delete-orphan')
    issues = relationship('VehicleIssue', back_populates='vehicle', cascade='all, delete-orphan')
    maintenance_history = relationship('VehicleMaintenanceHistory', back_populates='vehicle', cascade='all, delete-orphan')
    maintenance_configs = relationship('VehicleMaintenanceConfig', back_populates='vehicle', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Vehicle {self.plate} - {self.brand} {self.model}>"

    def get_current_km(self, db):
        """Obtém a quilometragem atual através do último log"""
        from app.models.vehicle_km_log import VehicleKmLog
        last_log = db.query(VehicleKmLog).filter(
            VehicleKmLog.vehicle_id == self.id
        ).order_by(VehicleKmLog.created_at.desc()).first()

        return last_log.current_km if last_log else 0

    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'plate': self.plate,
            'model': self.model,
            'brand': self.brand,
            'year': self.year,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
