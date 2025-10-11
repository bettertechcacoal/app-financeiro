# -*- coding: utf-8 -*-
from app.models.database import SessionLocal
from app.models.client import Client
from app.models.organization import Organization


class ClientService:
    """Serviço para gerenciamento de clientes"""

    def get_all_clients(self):
        """Retorna todos os clientes com suas organizações vinculadas"""
        db = SessionLocal()
        try:
            clients = db.query(Client).order_by(Client.name).all()
            return [client.to_dict(include_organizations=True) for client in clients]
        finally:
            db.close()

    def get_client_by_id(self, client_id):
        """Busca um cliente pelo ID com suas organizações vinculadas"""
        db = SessionLocal()
        try:
            client = db.query(Client).filter_by(id=client_id).first()
            return client.to_dict(include_organizations=True) if client else None
        finally:
            db.close()

    def create_client(self, client_data):
        """Cria um novo cliente"""
        db = SessionLocal()
        try:
            client = Client(
                name=client_data.get('name'),
                email=client_data.get('email'),
                phone=client_data.get('phone'),
                document=client_data.get('document'),
                address=client_data.get('address'),
                city=client_data.get('city'),
                state=client_data.get('state'),
                zipcode=client_data.get('zipcode'),
                billing_cycle_type=client_data.get('billing_cycle_type'),
                fixed_start_day=client_data.get('fixed_start_day')
            )
            db.add(client)
            db.commit()
            db.refresh(client)
            return client.to_dict()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def update_client(self, client_id, client_data):
        """Atualiza um cliente"""
        db = SessionLocal()
        try:
            client = db.query(Client).filter_by(id=client_id).first()
            if not client:
                return None

            client.name = client_data.get('name', client.name)
            client.email = client_data.get('email', client.email)
            client.phone = client_data.get('phone', client.phone)
            client.document = client_data.get('document', client.document)
            client.address = client_data.get('address', client.address)
            client.city = client_data.get('city', client.city)
            client.state = client_data.get('state', client.state)
            client.zipcode = client_data.get('zipcode', client.zipcode)
            client.billing_cycle_type = client_data.get('billing_cycle_type', client.billing_cycle_type)
            client.fixed_start_day = client_data.get('fixed_start_day', client.fixed_start_day)

            db.commit()
            db.refresh(client)
            return client.to_dict()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def delete_client(self, client_id):
        """Remove um cliente"""
        db = SessionLocal()
        try:
            client = db.query(Client).filter_by(id=client_id).first()
            if not client:
                return False

            db.delete(client)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def get_organizations(self):
        """Retorna todas as organizações do banco local"""
        db = SessionLocal()
        try:
            organizations = db.query(Organization).filter_by(is_active=True).order_by(Organization.business_name).all()
            return [org.to_dict() for org in organizations]
        finally:
            db.close()


# Instância singleton do serviço
client_service = ClientService()
