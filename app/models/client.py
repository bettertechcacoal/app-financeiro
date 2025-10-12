# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class Client(Base):
    """Modelo de Cliente"""
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50))
    document = Column(String(50), nullable=False, unique=True)

    # FK para organization (mantido por compatibilidade, mas usar tabela pivot)
    organization_id = Column(String(50))

    # Endereço
    address = Column(String(500))
    city_id = Column(Integer, ForeignKey('cities.id'))
    city = relationship('City', backref='clients')
    state = Column(String(2))
    zipcode = Column(String(20))

    # Ciclo de cobrança
    billing_cycle = Column(Integer)  # Ciclo de cobrança em dias
    billing_day = Column(Integer)  # Dia do mês para cobrança
    billing_cycle_type = Column(String(20))  # Tipo de ciclo: 'fixo' ou 'mensal'
    fixed_start_day = Column(Integer)  # Dia de início do ciclo fixo (1-31)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def to_dict(self, include_organizations=True):
        """Converte o modelo para dicionário

        Args:
            include_organizations: Se True, inclui lista de organizações vinculadas (padrão: True)
        """
        result = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'document': self.document,
            'organization_id': self.organization_id,
            'address': self.address,
            'city_id': self.city_id,
            'city': self.city.name if self.city else None,
            'state': self.state,
            'zipcode': self.zipcode,
            'billing_cycle': self.billing_cycle,
            'billing_day': self.billing_day,
            'billing_cycle_type': self.billing_cycle_type,
            'fixed_start_day': self.fixed_start_day,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        # Buscar organizações vinculadas via many-to-many
        result['organizations'] = []
        result['organization_name'] = None
        result['organization_id'] = None

        if include_organizations:
            from app.models.client_organization import ClientOrganization
            from app.models.organization import Organization
            from app.models.database import db_session

            org_links = db_session.query(ClientOrganization).filter_by(client_id=self.id).all()

            for link in org_links:
                org = db_session.query(Organization).filter_by(id=link.organization_id).first()
                if org:
                    result['organizations'].append({
                        'id': org.id,
                        'business_name': org.business_name,
                        'person_type': org.person_type
                    })

            # Define a primeira organização como padrão para views que mostram apenas uma
            if result['organizations']:
                result['organization_name'] = result['organizations'][0]['business_name']
                result['organization_id'] = result['organizations'][0]['id']

        return result
