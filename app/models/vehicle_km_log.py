# -*- coding: utf-8 -*-
"""
Model: VehicleKmLog
Representa registros de quilometragem dos veículos
"""

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class VehicleKmLog(Base):
    """Model para logs de quilometragem"""
    __tablename__ = 'vehicle_km_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id', ondelete='CASCADE'), nullable=False, comment='ID do veículo')
    travel_id = Column(Integer, ForeignKey('travels.id', ondelete='SET NULL'), nullable=True, comment='ID da viagem relacionada')
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, comment='ID do usuário que registrou')
    previous_km = Column(Integer, nullable=False, comment='Quilometragem anterior')
    current_km = Column(Integer, nullable=False, comment='Quilometragem atual')
    km_traveled = Column(Integer, nullable=False, comment='Quilômetros rodados')
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment='Data de criação')

    # Relationships
    vehicle = relationship('Vehicle', back_populates='km_logs')
    travel = relationship('Travel', foreign_keys=[travel_id])
    user = relationship('User', foreign_keys=[user_id])

    def __repr__(self):
        return f"<VehicleKmLog vehicle_id={self.vehicle_id} {self.previous_km}→{self.current_km}km>"

    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'travel_id': self.travel_id,
            'user_id': self.user_id,
            'previous_km': self.previous_km,
            'current_km': self.current_km,
            'km_traveled': self.km_traveled,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
