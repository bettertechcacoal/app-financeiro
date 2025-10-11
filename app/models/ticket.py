# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from app.models.database import Base


class Ticket(Base):
    """Modelo de Ticket do Movidesk"""
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    subject = Column(String(500))
    status = Column(String(100))
    category = Column(String(100))  # Categoria do ticket (Incidente, Dúvida, etc)
    service_full = Column(String(500))
    organization_name = Column(String(255))
    client_name = Column(String(255))
    owner_name = Column(String(255))
    created_by_name = Column(String(255))
    created_by_email = Column(String(255))
    created_date = Column(DateTime)  # Data e hora de abertura
    resolved_in = Column(DateTime)  # Data e hora de resolução do chat (encerramento pelo agente)
    closed_in = Column(DateTime)  # Data e hora de fechamento oficial
    custom_field_module = Column(String(255))
    synced_at = Column(DateTime, server_default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'status': self.status,
            'category': self.category,
            'serviceFull': self.service_full,
            'organizationName': self.organization_name,
            'clientName': self.client_name,
            'ownerName': self.owner_name,
            'createdByName': self.created_by_name,
            'createdByEmail': self.created_by_email,
            'createdDate': self.created_date.isoformat() if self.created_date else None,
            'resolvedIn': self.resolved_in.isoformat() if self.resolved_in else None,
            'closedIn': self.closed_in.isoformat() if self.closed_in else None,
            'customFieldModule': self.custom_field_module,
            'syncedAt': self.synced_at.isoformat() if self.synced_at else None
        }
