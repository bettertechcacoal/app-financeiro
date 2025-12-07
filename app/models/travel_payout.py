# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class TravelPayout(Base):
    """Modelo de Repasses Financeiros de Viagem - controle de valores por participante"""
    __tablename__ = 'travel_payouts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    travel_id = Column(Integer, ForeignKey('travels.id', ondelete='CASCADE'), nullable=False)
    member_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False, default=0)
    payout_history = Column(JSONB, nullable=True, default=list, comment='Histórico de lançamentos em JSONB')
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
            'payout_history': self.payout_history if self.payout_history else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
