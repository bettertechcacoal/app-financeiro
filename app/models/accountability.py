# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, String, Enum, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base
import enum


class AccountabilityStatus(enum.Enum):
    """Status da prestação de contas"""
    DRAFT = "draft"  # Rascunho
    SUBMITTED = "submitted"  # Enviado para análise
    RETURNED = "returned"  # Devolvido para revisão
    APPROVED = "approved"  # Aprovado


class Accountability(Base):
    """Modelo de Prestação de Contas - armazena dados detalhados da prestação"""
    __tablename__ = 'accountabilities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    payout_id = Column(Integer, ForeignKey('travel_payouts.id', ondelete='CASCADE'), nullable=False, unique=True)

    # Dados da prestação de contas
    accommodation_expense = Column(Numeric(10, 2), default=0.00)  # Hospedagem
    accommodation_receipt = Column(String(500))  # Comprovante de hospedagem

    food_expense = Column(Numeric(10, 2), default=0.00)  # Alimentação
    food_receipt = Column(String(500))  # Comprovante de alimentação

    transport_expense = Column(Numeric(10, 2), default=0.00)  # Transporte
    transport_receipt = Column(String(500))  # Comprovante de transporte

    fuel_expense = Column(Numeric(10, 2), default=0.00)  # Combustível
    fuel_receipt = Column(String(500))  # Comprovante de combustível

    toll_expense = Column(Numeric(10, 2), default=0.00)  # Pedágio
    toll_receipt = Column(String(500))  # Comprovante de pedágio

    parking_expense = Column(Numeric(10, 2), default=0.00)  # Estacionamento
    parking_receipt = Column(String(500))  # Comprovante de estacionamento

    other_expense = Column(Numeric(10, 2), default=0.00)  # Outras despesas
    other_receipt = Column(String(500))  # Comprovante de outras despesas
    other_description = Column(Text)  # Descrição de outras despesas

    # Campos adicionais
    observations = Column(Text)  # Observações gerais
    additional_data = Column(JSON)  # Dados adicionais em formato JSON

    # Controle de status
    status = Column(Enum(AccountabilityStatus), default=AccountabilityStatus.DRAFT, nullable=False)
    submitted_at = Column(DateTime(timezone=True))  # Data de envio
    reviewed_at = Column(DateTime(timezone=True))  # Data de revisão
    approved_at = Column(DateTime(timezone=True))  # Data de aprovação
    reviewed_by = Column(Integer, ForeignKey('users.id'))  # Quem revisou

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamentos
    payout = relationship('TravelPayout', backref='accountability')
    reviewer = relationship('User', foreign_keys=[reviewed_by])
    history = relationship('AccountabilityHistory', back_populates='accountability', cascade='all, delete-orphan')

    @property
    def total_expense(self):
        """Calcula o total de despesas"""
        return (
            (self.accommodation_expense or 0) +
            (self.food_expense or 0) +
            (self.transport_expense or 0) +
            (self.fuel_expense or 0) +
            (self.toll_expense or 0) +
            (self.parking_expense or 0) +
            (self.other_expense or 0)
        )

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'payout_id': self.payout_id,
            'accommodation_expense': float(self.accommodation_expense) if self.accommodation_expense else 0.0,
            'accommodation_receipt': self.accommodation_receipt,
            'food_expense': float(self.food_expense) if self.food_expense else 0.0,
            'food_receipt': self.food_receipt,
            'transport_expense': float(self.transport_expense) if self.transport_expense else 0.0,
            'transport_receipt': self.transport_receipt,
            'fuel_expense': float(self.fuel_expense) if self.fuel_expense else 0.0,
            'fuel_receipt': self.fuel_receipt,
            'toll_expense': float(self.toll_expense) if self.toll_expense else 0.0,
            'toll_receipt': self.toll_receipt,
            'parking_expense': float(self.parking_expense) if self.parking_expense else 0.0,
            'parking_receipt': self.parking_receipt,
            'other_expense': float(self.other_expense) if self.other_expense else 0.0,
            'other_receipt': self.other_receipt,
            'other_description': self.other_description,
            'observations': self.observations,
            'additional_data': self.additional_data,
            'status': self.status.value if self.status else None,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'reviewed_by': self.reviewed_by,
            'reviewer': self.reviewer.to_dict() if self.reviewer else None,
            'total_expense': float(self.total_expense),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
