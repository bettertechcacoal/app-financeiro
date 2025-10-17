# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base
import enum


class StatementStatus(enum.Enum):
    """Status da prestação de contas"""
    DRAFT = "draft"  # Rascunho
    SUBMITTED = "submitted"  # Enviado para análise
    RETURNED = "returned"  # Devolvido para revisão
    APPROVED = "approved"  # Aprovado


class TravelStatement(Base):
    """Modelo de Prestação de Contas de Viagem"""
    __tablename__ = 'travel_statements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    payout_id = Column(Integer, ForeignKey('travel_payouts.id', ondelete='CASCADE'), nullable=False, unique=True)

    # Armazena todo o conteúdo da prestação em formato JSON
    statement_content = Column(JSON, nullable=True)

    # Status do workflow
    status = Column(Enum(StatementStatus, name='statementstatus', values_callable=lambda x: [e.value for e in x]), default=StatementStatus.DRAFT, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamentos
    payout = relationship('TravelPayout', backref='statement')

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'payout_id': self.payout_id,
            'statement_content': self.statement_content,
            'status': self.status.value if self.status else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
