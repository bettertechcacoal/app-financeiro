# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean, Table
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

    # Relacionamento com usuário motorista/viajante
    driver_user_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='ID do usuário motorista/viajante')
    driver_user = relationship('User', foreign_keys=[driver_user_id], back_populates='travels')

    # Relacionamento com cidade de destino
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False, comment='ID da cidade de destino')
    city = relationship('City', back_populates='travels')

    # Detalhes da viagem
    purpose = Column(String(255), nullable=False, comment='Motivo/propósito da viagem')
    departure_date = Column(DateTime(timezone=True), nullable=False, comment='Data e hora de saída')
    return_date = Column(DateTime(timezone=True), nullable=False, comment='Data e hora de retorno')
    needs_vehicle = Column(Boolean, default=False, nullable=False, comment='Indica se necessita reserva de veículo da frota')

    # Relacionamento com usuário que criou o registro
    record_user_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='ID do usuário que criou o registro')
    record_user = relationship('User', foreign_keys=[record_user_id])

    # Status e controle
    status = Column(Enum(TravelStatus, name='travelstatus', values_callable=lambda x: [e.value for e in x]), default=TravelStatus.PENDING, nullable=False)
    approved_by = Column(Integer, ForeignKey('users.id'))  # ID do usuário que aprovou
    approved_at = Column(DateTime(timezone=True))  # Data/hora da aprovação

    # Observações e notas
    notes = Column(Text)  # Observações gerais
    admin_notes = Column(Text)  # Notas administrativas (visível apenas para gestores)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamento com passageiros (many-to-many via travel_passengers)
    travel_passengers = relationship('TravelPassenger', back_populates='travel', cascade='all, delete-orphan')

    # Relacionamento com histórico de veículos
    vehicle_history = relationship('VehicleTravelHistory', back_populates='travel')

    # Relacionamento com repasses financeiros
    payouts = relationship('TravelPayout', back_populates='travel', cascade='all, delete-orphan')

    # Relacionamento com quem aprovou
    approved_by_user = relationship('User', foreign_keys=[approved_by])

    def to_dict(self):
        """Converte o modelo para dicionário"""
        # Pegar o veículo alocado (se houver) do histórico
        allocated_vehicle = None
        if self.vehicle_history:
            # Pegar o último registro de veículo para esta viagem
            allocated_vehicle = self.vehicle_history[-1].vehicle.to_dict() if self.vehicle_history[-1].vehicle else None

        return {
            'id': self.id,
            'driver_user_id': self.driver_user_id,
            'driver_user': self.driver_user.to_dict() if self.driver_user else None,
            'record_user_id': self.record_user_id,
            'record_user': self.record_user.to_dict() if self.record_user else None,
            'city_id': self.city_id,
            'city': self.city.to_dict() if self.city else None,
            'purpose': self.purpose,
            'departure_date': self.departure_date.isoformat() if self.departure_date else None,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'needs_vehicle': self.needs_vehicle,
            'status': self.status.value if self.status else None,
            'approved_by': self.approved_by,
            'approved_by_user': self.approved_by_user.to_dict() if self.approved_by_user else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'notes': self.notes,
            'admin_notes': self.admin_notes,
            'passengers': [tp.user.to_dict() if tp.user else None for tp in self.travel_passengers] if self.travel_passengers else [],
            'vehicle': allocated_vehicle,  # Veículo alocado através do histórico
            'payouts': [payout.to_dict() for payout in self.payouts] if self.payouts else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
