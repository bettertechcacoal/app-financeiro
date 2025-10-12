# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class TravelPassenger(Base):
    """Modelo de Passageiros de Viagem - relacionamento many-to-many"""
    __tablename__ = 'travel_passengers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    travel_id = Column(Integer, ForeignKey('travels.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relacionamentos
    travel = relationship('Travel', back_populates='travel_passengers')
    user = relationship('User', foreign_keys=[user_id])

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'travel_id': self.travel_id,
            'user_id': self.user_id,
            'user': self.user.to_dict() if self.user else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
