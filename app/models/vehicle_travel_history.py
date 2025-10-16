# -*- coding: utf-8 -*-
"""
Model: VehicleTravelHistory
Representa o histórico de viagens dos veículos
"""

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class VehicleTravelHistory(Base):
    """Model para histórico de viagens de veículos"""
    __tablename__ = 'vehicle_travel_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id', ondelete='CASCADE'), nullable=False, comment='ID do veículo')
    travel_id = Column(Integer, ForeignKey('travels.id', ondelete='SET NULL'), nullable=True, comment='ID da viagem relacionada')
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, comment='ID do usuário que registrou')
    previous_km = Column(Integer, nullable=False, comment='Quilometragem anterior')
    current_km = Column(Integer, nullable=False, comment='Quilometragem atual')
    km_traveled = Column(Integer, nullable=False, comment='Quilômetros rodados')
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment='Data de criação')

    # Relationships
    vehicle = relationship('Vehicle')
    travel = relationship('Travel')
    user = relationship('User')

    def __repr__(self):
        return f"<VehicleTravelHistory vehicle_id={self.vehicle_id} travel_id={self.travel_id}>"

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
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'vehicle': self.vehicle.to_dict() if self.vehicle else None,
            'travel': self.travel.to_dict() if self.travel else None,
            'user': self.user.to_dict() if self.user else None
        }
