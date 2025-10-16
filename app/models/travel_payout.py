# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base
import enum


class PayoutStatus(enum.Enum):
    """Status do repasse financeiro"""
    PENDING = "pending"  # Aguardando repasse
    PAID = "paid"  # Repasse concluído
    CANCELLED = "cancelled"  # Repasse cancelado


class TravelPayout(Base):
    """Modelo de Repasses Financeiros de Viagem - controle de valores por participante"""
    __tablename__ = 'travel_payouts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    travel_id = Column(Integer, ForeignKey('travels.id', ondelete='CASCADE'), nullable=False)
    member_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(PayoutStatus), default=PayoutStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamentos
    travel = relationship('Travel', back_populates='payouts')
    member = relationship('User', foreign_keys=[member_id])

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'travel_id': self.travel_id,
            'member_id': self.member_id,
            'member': self.member.to_dict() if self.member else None,
            'amount': float(self.amount) if self.amount else 0.0,
            'status': self.status.value if self.status else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
