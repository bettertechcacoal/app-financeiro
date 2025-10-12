# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base
import enum


class NotificationType(enum.Enum):
    """Tipos de notificação"""
    INFO = "info"  # Informação geral
    SUCCESS = "success"  # Sucesso
    WARNING = "warning"  # Aviso
    ERROR = "error"  # Erro
    TRAVEL = "travel"  # Relacionado a viagens
    TICKET = "ticket"  # Relacionado a tickets
    SYSTEM = "system"  # Sistema


class Notification(Base):
    """Modelo de Notificação"""
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Relacionamento com usuário
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', foreign_keys=[user_id])

    # Conteúdo da notificação
    title = Column(String(255), nullable=False)  # Título da notificação
    message = Column(Text, nullable=False)  # Mensagem detalhada
    type = Column(Enum(NotificationType), default=NotificationType.INFO, nullable=False)  # Tipo

    # Link de ação (opcional)
    action_url = Column(String(500), nullable=True)  # URL para redirecionar ao clicar
    action_text = Column(String(100), nullable=True)  # Texto do botão de ação

    # Controle de leitura
    is_read = Column(Boolean, default=False, nullable=False)  # Se foi lida
    read_at = Column(DateTime(timezone=True), nullable=True)  # Quando foi lida

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'type': self.type.value if self.type else None,
            'action_url': self.action_url,
            'action_text': self.action_text,
            'is_read': self.is_read,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
