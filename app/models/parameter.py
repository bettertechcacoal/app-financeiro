# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base
import enum


class ParameterType(enum.Enum):
    """Tipos de parâmetros"""
    TEXT = "text"  # Campo de texto livre
    CHECKBOX = "checkbox"  # Checkbox (S/N)
    SELECT = "select"  # Select com opções pré-definidas


class Parameter(Base):
    """Modelo de Parâmetros do Sistema"""
    __tablename__ = 'parameters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    parameter = Column(String(100), unique=True, nullable=False)  # Nome do parâmetro (ex: MOVIDESK_TOKEN)
    type = Column(Enum(ParameterType), default=ParameterType.TEXT, nullable=False)  # Tipo do parâmetro
    description = Column(String(255), nullable=False)  # Descrição do parâmetro
    value = Column(Text)  # Valor do parâmetro (pode ser texto, JSON, etc)
    options = Column(Text)  # Opções disponíveis para o tipo SELECT (JSON array, ex: ["opcao1", "opcao2"])
    group_id = Column(Integer, ForeignKey('parameter_groups.id'))  # Grupo do parâmetro

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamento com grupo
    group = relationship('ParameterGroup', back_populates='parameters')

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'parameter': self.parameter,
            'type': self.type.value if self.type else None,
            'description': self.description,
            'value': self.value,
            'options': self.options,
            'group_id': self.group_id,
            'group': self.group.to_dict() if self.group else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def get_value(db, parameter_name, default=None):
        """
        Método auxiliar para obter o valor de um parâmetro

        Args:
            db: Sessão do banco de dados
            parameter_name: Nome do parâmetro
            default: Valor padrão caso não encontre

        Returns:
            Valor do parâmetro ou default
        """
        param = db.query(Parameter).filter_by(parameter=parameter_name).first()
        return param.value if param else default

    @staticmethod
    def set_value(db, parameter_name, value):
        """
        Método auxiliar para definir o valor de um parâmetro

        Args:
            db: Sessão do banco de dados
            parameter_name: Nome do parâmetro
            value: Novo valor

        Returns:
            True se atualizado, False se não encontrado
        """
        param = db.query(Parameter).filter_by(parameter=parameter_name).first()
        if param:
            param.value = value
            db.commit()
            return True
        return False
