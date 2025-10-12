# -*- coding: utf-8 -*-
from app.models.database import SessionLocal
from app.models.client import Client
from app.models.client_meta import ClientMeta
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
        """Busca um cliente pelo ID com suas organizações vinculadas e meta dados"""
        db = SessionLocal()
        try:
            client = db.query(Client).filter_by(id=client_id).first()
            if not client:
                return None

            client_dict = client.to_dict(include_organizations=True)

            # Adicionar meta dados
            metas = db.query(ClientMeta).filter_by(client_id=client_id).all()
            client_dict['meta'] = {meta.meta_key: meta.meta_value for meta in metas}

            return client_dict
        finally:
            db.close()

    def create_client(self, client_data):
        """Cria um novo cliente"""
        db = SessionLocal()
        try:
            from app.models.city import City

            # Converter nome da cidade em city_id
            city_id = None
            city_name = client_data.get('city')
            if city_name:
                city_obj = db.query(City).filter_by(name=city_name).first()
                if city_obj:
                    city_id = city_obj.id

            client = Client(
                name=client_data.get('name'),
                email=client_data.get('email'),
                phone=client_data.get('phone'),
                document=client_data.get('document'),
                address=client_data.get('address'),
                city_id=city_id,
                state=client_data.get('state'),
                zipcode=client_data.get('zipcode'),
                billing_cycle=client_data.get('billing_cycle'),
                billing_day=client_data.get('billing_day'),
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
            from app.models.city import City

            client = db.query(Client).filter_by(id=client_id).first()
            if not client:
                return None

            client.name = client_data.get('name', client.name)
            client.email = client_data.get('email', client.email)
            client.phone = client_data.get('phone', client.phone)
            client.document = client_data.get('document', client.document)
            client.address = client_data.get('address', client.address)

            # Converter nome da cidade em city_id
            city_name = client_data.get('city')
            if city_name:
                city_obj = db.query(City).filter_by(name=city_name).first()
                if city_obj:
                    client.city_id = city_obj.id

            client.state = client_data.get('state', client.state)
            client.zipcode = client_data.get('zipcode', client.zipcode)
            client.billing_cycle = client_data.get('billing_cycle', client.billing_cycle)
            client.billing_day = client_data.get('billing_day', client.billing_day)
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

    def get_client_meta(self, client_id, meta_key=None):
        """Retorna meta dados de um cliente

        Args:
            client_id: ID do cliente
            meta_key: Chave específica para buscar (opcional)

        Returns:
            dict: Dicionário com meta_key como chave e meta_value como valor
                  ou None se meta_key for especificada e não existir
        """
        db = SessionLocal()
        try:
            if meta_key:
                meta = db.query(ClientMeta).filter_by(
                    client_id=client_id,
                    meta_key=meta_key
                ).first()
                return meta.meta_value if meta else None
            else:
                metas = db.query(ClientMeta).filter_by(client_id=client_id).all()
                return {meta.meta_key: meta.meta_value for meta in metas}
        finally:
            db.close()

    def update_client_meta(self, client_id, meta_key, meta_value):
        """Atualiza ou cria um meta dado do cliente

        Args:
            client_id: ID do cliente
            meta_key: Chave do meta dado
            meta_value: Valor do meta dado

        Returns:
            bool: True se sucesso
        """
        db = SessionLocal()
        try:
            # Buscar meta existente
            meta = db.query(ClientMeta).filter_by(
                client_id=client_id,
                meta_key=meta_key
            ).first()

            if meta:
                # Atualizar existente
                meta.meta_value = meta_value
            else:
                # Criar novo
                meta = ClientMeta(
                    client_id=client_id,
                    meta_key=meta_key,
                    meta_value=meta_value
                )
                db.add(meta)

            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def delete_client_meta(self, client_id, meta_key):
        """Remove um meta dado do cliente

        Args:
            client_id: ID do cliente
            meta_key: Chave do meta dado

        Returns:
            bool: True se removido com sucesso
        """
        db = SessionLocal()
        try:
            meta = db.query(ClientMeta).filter_by(
                client_id=client_id,
                meta_key=meta_key
            ).first()

            if meta:
                db.delete(meta)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def update_client_metas(self, client_id, metas_dict):
        """Atualiza múltiplos meta dados de uma vez

        Args:
            client_id: ID do cliente
            metas_dict: Dicionário com meta_key: meta_value

        Returns:
            bool: True se sucesso
        """
        db = SessionLocal()
        try:
            for meta_key, meta_value in metas_dict.items():
                # Buscar meta existente
                meta = db.query(ClientMeta).filter_by(
                    client_id=client_id,
                    meta_key=meta_key
                ).first()

                if meta:
                    # Atualizar existente
                    meta.meta_value = meta_value
                else:
                    # Criar novo
                    meta = ClientMeta(
                        client_id=client_id,
                        meta_key=meta_key,
                        meta_value=meta_value
                    )
                    db.add(meta)

            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()


# Instância singleton do serviço
client_service = ClientService()
