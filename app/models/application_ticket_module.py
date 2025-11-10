# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.models.database import Base


class ApplicationTicketModule(Base):
    """Modelo de Associação entre Application e TicketModule (Many-to-Many)"""
    __tablename__ = 'application_ticket_module'

    id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey('applications.id', ondelete='CASCADE'), nullable=False)
    ticket_module_id = Column(Integer, ForeignKey('tickets_modules.id', ondelete='CASCADE'), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'application_id': self.application_id,
            'ticket_module_id': self.ticket_module_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
