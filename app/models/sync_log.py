# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.models.database import Base


class SyncLog(Base):
    """Modelo de Log de Sincronização"""
    __tablename__ = 'sync_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sync_type = Column(String(50), nullable=False)  # 'organizations', 'tickets', etc
    total = Column(Integer, default=0)
    synced = Column(Integer, default=0)  # Novos
    updated = Column(Integer, default=0)  # Atualizados
    errors = Column(Integer, default=0)
    synced_at = Column(DateTime, server_default=func.now())

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'sync_type': self.sync_type,
            'total': self.total,
            'synced': self.synced,
            'updated': self.updated,
            'errors': self.errors,
            'synced_at': self.synced_at.isoformat() if self.synced_at else None
        }
