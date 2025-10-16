# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base
from app.models.accountability import AccountabilityStatus


class AccountabilityHistory(Base):
    """Modelo de Histórico de Prestação de Contas - rastreia mudanças de status"""
    __tablename__ = 'accountability_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    accountability_id = Column(Integer, ForeignKey('accountabilities.id', ondelete='CASCADE'), nullable=False)

    # Status anterior e novo
    from_status = Column(Enum(AccountabilityStatus), nullable=True)  # Status anterior (NULL na criação)
    to_status = Column(Enum(AccountabilityStatus), nullable=False)  # Novo status

    # Informações da mudança
    comment = Column(Text)  # Comentário/motivo da mudança
    changed_by = Column(Integer, ForeignKey('users.id'), nullable=False)  # Quem fez a mudança

    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relacionamentos
    accountability = relationship('Accountability', back_populates='history')
    user = relationship('User', foreign_keys=[changed_by])

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'accountability_id': self.accountability_id,
            'from_status': self.from_status.value if self.from_status else None,
            'to_status': self.to_status.value if self.to_status else None,
            'comment': self.comment,
            'changed_by': self.changed_by,
            'user': self.user.to_dict() if self.user else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
