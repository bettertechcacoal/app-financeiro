# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Date, JSON
from app.models.database import Base


class License(Base):
    """Modelo para armazenar licenças de sistemas (dados brutos dos TXT)"""
    __tablename__ = 'licenses'

    id = Column(Integer, primary_key=True)
    client_code = Column(String(50), nullable=False)  # Código do cliente (ex: 57001)
    client_name = Column(String(255), nullable=False)  # Nome do cliente
    license_date = Column(Date, nullable=False)  # Data da licença
    module_code = Column(String(200), nullable=False)  # Código do módulo (ex: APICE - Orçamento, OXY Folha de Pagamento)
    password = Column(String(100), nullable=False)  # Senha do sistema

    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'client_code': self.client_code,
            'client_name': self.client_name,
            'license_date': self.license_date.strftime('%Y-%m-%d') if self.license_date else None,
            'module_code': self.module_code,
            'password': self.password
        }
