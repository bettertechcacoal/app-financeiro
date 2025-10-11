# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base
import enum


class TravelStatus(enum.Enum):
    """Status da viagem"""
    PENDING = "pending"  # Pendente
    APPROVED = "approved"  # Aprovada
    IN_PROGRESS = "in_progress"  # Em andamento
    COMPLETED = "completed"  # Concluída
    CANCELLED = "cancelled"  # Cancelada


class Travel(Base):
    """Modelo de Viagem - padrão Laravel"""
    __tablename__ = 'travels'

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Relacionamento com usuário
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', foreign_keys=[user_id], back_populates='travels')

    # Relacionamento com cidade de destino
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    city = relationship('City', back_populates='travels')

    # Detalhes da viagem
    purpose = Column(String(255), nullable=False)  # Motivo da viagem
    description = Column(Text)  # Descrição detalhada
    departure_date = Column(DateTime(timezone=True), nullable=False)  # Data/hora de saída
    return_date = Column(DateTime(timezone=True), nullable=False)  # Data/hora de retorno

    # Status e controle
    status = Column(Enum(TravelStatus), default=TravelStatus.PENDING, nullable=False)
    approved_by = Column(Integer, ForeignKey('users.id'))  # ID do usuário que aprovou
    approved_at = Column(DateTime(timezone=True))  # Data/hora da aprovação

    # Observações e notas
    notes = Column(Text)  # Observações gerais
    admin_notes = Column(Text)  # Notas administrativas (visível apenas para gestores)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user': self.user.to_dict() if self.user else None,
            'city_id': self.city_id,
            'city': self.city.to_dict() if self.city else None,
            'purpose': self.purpose,
            'description': self.description,
            'departure_date': self.departure_date.isoformat() if self.departure_date else None,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'status': self.status.value if self.status else None,
            'approved_by': self.approved_by,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'notes': self.notes,
            'admin_notes': self.admin_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
