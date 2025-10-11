# -*- coding: utf-8 -*-
import requests
import os
from datetime import datetime, timedelta
from app.models.database import SessionLocal
from app.models.organization import Organization
from app.models.ticket import Ticket
from app.models.sync_log import SyncLog


class MovideskService:
    """Serviço para integração com a API do Movidesk"""

    def __init__(self):
        self.token = os.getenv('MOVIDESK_TOKEN')
        self.base_url = "https://api.movidesk.com/public/v1"

    def get_organizations_from_api(self):
        """Busca organizações diretamente da API do Movidesk"""
        try:
            url = f"{self.base_url}/persons"
            params = {
                'token': self.token,
                '$select': 'id,businessName,personType',
                '$filter': 'personType eq 2 and isActive eq true',
                '$orderby': 'businessName'
            }

            response = requests.get(url, params=params, timeout=60)
            response.raise_for_status()

            return response.json()
        except Exception as e:
            print(f"Erro ao buscar organizações do Movidesk: {e}")
            raise Exception(f"Erro ao buscar organizações: {str(e)}")

    def sync_organizations(self):
        """Sincroniza organizações do Movidesk com o banco de dados local"""
        try:
            # Busca organizações da API
            organizations_data = self.get_organizations_from_api()

            db = SessionLocal()
            synced_count = 0
            updated_count = 0
            errors = []

            for org_data in organizations_data:
                try:
                    org_id = org_data.get('id')

                    # Verifica se a organização já existe
                    existing_org = db.query(Organization).filter_by(id=org_id).first()

                    if existing_org:
                        # Atualiza organização existente
                        existing_org.business_name = org_data.get('businessName')
                        existing_org.person_type = str(org_data.get('personType'))
                        existing_org.is_active = True
                        updated_count += 1
                    else:
                        # Cria nova organização
                        new_org = Organization(
                            id=org_id,
                            business_name=org_data.get('businessName'),
                            person_type=str(org_data.get('personType')),
                            is_active=True
                        )
                        db.add(new_org)
                        synced_count += 1

                    db.commit()

                except Exception as e:
                    db.rollback()
                    errors.append(f"Organização {org_data.get('id')}: {str(e)}")

            # Salvar log de sincronização
            sync_log = SyncLog(
                sync_type='organizations',
                total=len(organizations_data),
                synced=synced_count,
                updated=updated_count,
                errors=len(errors)
            )
            db.add(sync_log)
            db.commit()

            db.close()

            return {
                'success': True,
                'total': len(organizations_data),
                'synced': synced_count,
                'updated': updated_count,
                'errors': len(errors),
                'error_details': errors[:10]
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_local_organizations(self):
        """Retorna organizações do banco de dados local"""
        db = SessionLocal()
        try:
            organizations = db.query(Organization).filter_by(is_active=True).order_by(Organization.business_name).all()
            return [org.to_dict() for org in organizations]
        finally:
            db.close()

    def get_organization_by_id(self, org_id):
        """Busca uma organização pelo ID"""
        db = SessionLocal()
        try:
            org = db.query(Organization).filter_by(id=org_id).first()
            return org.to_dict() if org else None
        finally:
            db.close()

    def get_organizations_stats(self):
        """Retorna estatísticas sobre as organizações"""
        db = SessionLocal()
        try:
            total = db.query(Organization).filter_by(is_active=True).count()

            # Buscar última sincronização
            last_sync = db.query(SyncLog).filter_by(sync_type='organizations').order_by(SyncLog.synced_at.desc()).first()

            return {
                'total': total,
                'active': total,  # Todas as organizações são ativas
                'last_sync': last_sync.to_dict() if last_sync else None
            }
        finally:
            db.close()

    def get_tickets_from_api(self, start_date, end_date):
        """Busca tickets diretamente da API do Movidesk"""
        try:
            select_fields = "id,subject,status,category,createdDate,owner,resolvedIn,closedIn,serviceFull"
            filter_query = f"createdDate gt {start_date}T00:00:00.00z and createdDate le {end_date}T23:59:59.99z"
            expand = "owner,createdBy,clients($select=businessName),clients($expand=organization),customFieldValues($expand=items)"

            url = f"{self.base_url}/tickets"
            params = {
                'token': self.token,
                '$select': select_fields,
                '$filter': filter_query,
                '$expand': expand
            }

            response = requests.get(url, params=params, timeout=120)
            response.raise_for_status()

            return response.json()
        except Exception as e:
            print(f"Erro ao buscar tickets do Movidesk: {e}")
            raise Exception(f"Erro ao buscar tickets: {str(e)}")

    def sync_tickets(self, start_date, end_date):
        """Sincroniza tickets do Movidesk com o banco de dados local"""
        try:
            # Validar período (máximo 5 dias)
            date_start = datetime.strptime(start_date, '%Y-%m-%d')
            date_end = datetime.strptime(end_date, '%Y-%m-%d')

            if (date_end - date_start).days > 5:
                return {
                    'success': False,
                    'error': 'O período não pode ser maior que 5 dias'
                }

            # Busca tickets da API
            tickets_data = self.get_tickets_from_api(start_date, end_date)

            db = SessionLocal()
            synced_count = 0
            updated_count = 0
            errors = []

            for ticket_data in tickets_data:
                try:
                    ticket_id = ticket_data.get('id')

                    # Processa os dados do ticket
                    ticket_info = self._parse_ticket(ticket_data)

                    # Verifica se o ticket já existe
                    existing_ticket = db.query(Ticket).filter_by(id=ticket_id).first()

                    if existing_ticket:
                        # Atualiza ticket existente
                        existing_ticket.subject = ticket_info['subject']
                        existing_ticket.status = ticket_info['status']
                        existing_ticket.category = ticket_info['category']
                        existing_ticket.service_full = ticket_info['service_full']
                        existing_ticket.organization_name = ticket_info['organization_name']
                        existing_ticket.client_name = ticket_info['client_name']
                        existing_ticket.owner_name = ticket_info['owner_name']
                        existing_ticket.created_by_name = ticket_info['created_by_name']
                        existing_ticket.created_by_email = ticket_info['created_by_email']
                        existing_ticket.created_date = ticket_info['created_date']
                        existing_ticket.resolved_in = ticket_info['resolved_in']
                        existing_ticket.closed_in = ticket_info['closed_in']
                        existing_ticket.custom_field_module = ticket_info['custom_field_module']
                        updated_count += 1
                    else:
                        # Cria novo ticket
                        new_ticket = Ticket(
                            id=ticket_id,
                            subject=ticket_info['subject'],
                            status=ticket_info['status'],
                            category=ticket_info['category'],
                            service_full=ticket_info['service_full'],
                            organization_name=ticket_info['organization_name'],
                            client_name=ticket_info['client_name'],
                            owner_name=ticket_info['owner_name'],
                            created_by_name=ticket_info['created_by_name'],
                            created_by_email=ticket_info['created_by_email'],
                            created_date=ticket_info['created_date'],
                            resolved_in=ticket_info['resolved_in'],
                            closed_in=ticket_info['closed_in'],
                            custom_field_module=ticket_info['custom_field_module']
                        )
                        db.add(new_ticket)
                        synced_count += 1

                    db.commit()

                except Exception as e:
                    db.rollback()
                    errors.append(f"Ticket {ticket_data.get('id')}: {str(e)}")

            # Salvar log de sincronização
            sync_log = SyncLog(
                sync_type='tickets',
                total=len(tickets_data),
                synced=synced_count,
                updated=updated_count,
                errors=len(errors)
            )
            db.add(sync_log)
            db.commit()

            db.close()

            return {
                'success': True,
                'total': len(tickets_data),
                'synced': synced_count,
                'updated': updated_count,
                'errors': len(errors),
                'error_details': errors[:10]
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _parse_ticket(self, ticket):
        """Converte ticket da API para formato do banco"""
        ticket_info = {
            'subject': ticket.get('subject'),
            'status': ticket.get('status'),
            'category': ticket.get('category'),
            'service_full': ', '.join(ticket.get('serviceFull', [])) if ticket.get('serviceFull') else None,
            'organization_name': None,
            'client_name': None,
            'owner_name': None,
            'created_by_name': None,
            'created_by_email': None,
            'created_date': None,
            'resolved_in': None,
            'closed_in': None,
            'custom_field_module': None
        }

        # Cliente e organização
        clients = ticket.get('clients', [])
        if clients:
            client = clients[0]
            ticket_info['client_name'] = client.get('businessName')

            organization = client.get('organization')
            if organization:
                ticket_info['organization_name'] = organization.get('businessName')
            else:
                ticket_info['organization_name'] = client.get('businessName')

        # Responsável
        owner = ticket.get('owner')
        if owner:
            ticket_info['owner_name'] = owner.get('businessName')

        # Criado por
        created_by = ticket.get('createdBy')
        if created_by:
            ticket_info['created_by_name'] = created_by.get('businessName')
            ticket_info['created_by_email'] = created_by.get('email')

        # Datas (mantém data e hora completas)
        created_date = ticket.get('createdDate')
        if created_date:
            ticket_info['created_date'] = datetime.fromisoformat(
                created_date.replace('Z', '+00:00')
            )

        resolved_in = ticket.get('resolvedIn')
        if resolved_in:
            ticket_info['resolved_in'] = datetime.fromisoformat(
                resolved_in.replace('Z', '+00:00')
            )

        closed_in = ticket.get('closedIn')
        if closed_in:
            ticket_info['closed_in'] = datetime.fromisoformat(
                closed_in.replace('Z', '+00:00')
            )

        # Módulo
        custom_fields = ticket.get('customFieldValues', [])
        if custom_fields:
            items = custom_fields[0].get('items', [])
            if items:
                ticket_info['custom_field_module'] = items[0].get('customFieldItem')

        return ticket_info

    def get_tickets_stats(self):
        """Retorna estatísticas sobre os tickets"""
        db = SessionLocal()
        try:
            total = db.query(Ticket).count()

            # Buscar última sincronização
            last_sync = db.query(SyncLog).filter_by(sync_type='tickets').order_by(SyncLog.synced_at.desc()).first()

            return {
                'total': total,
                'last_sync': last_sync.to_dict() if last_sync else None
            }
        finally:
            db.close()


# Instância singleton
movidesk_service = MovideskService()
