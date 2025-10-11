# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.models.database import Base


class Organization(Base):
    """Modelo de Organização (Movidesk)"""
    __tablename__ = 'organizations'

    id = Column(String(50), primary_key=True)  # ID do Movidesk
    business_name = Column(String(255), nullable=False)
    person_type = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'businessName': self.business_name,
            'personType': self.person_type,
            'isActive': self.is_active,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
