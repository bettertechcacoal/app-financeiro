# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from app.models.database import Base


class LicenseApplication(Base):
    """Modelo para armazenar mapeamento de códigos de módulos para nomes"""
    __tablename__ = 'license_applications'

    id = Column(Integer, primary_key=True)
    code = Column(String(10), unique=True, nullable=False)  # Código do módulo (002, 003, 101, 306, etc.)
    name = Column(String(200), nullable=False)  # Nome do módulo (APICE - Orçamento, etc.)

    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name
        }
