# -*- coding: utf-8 -*-
from app.models.database import SessionLocal
from app.models.ticket import Ticket
from sqlalchemy import func


class TicketService:
    """Serviço para gerenciamento de tickets"""

    def get_tickets_by_organization(self, organization_name):
        """Retorna todos os tickets de uma organização"""
        db = SessionLocal()
        try:
            tickets = db.query(Ticket).filter_by(organization_name=organization_name).order_by(Ticket.created_date.desc()).all()
            return [ticket.to_dict() for ticket in tickets]
        finally:
            db.close()

    def get_all_tickets(self):
        """Retorna todos os tickets"""
        db = SessionLocal()
        try:
            tickets = db.query(Ticket).order_by(Ticket.created_date.desc()).all()
            return [ticket.to_dict() for ticket in tickets]
        finally:
            db.close()

    def get_ticket_by_id(self, ticket_id):
        """Busca um ticket pelo ID"""
        db = SessionLocal()
        try:
            ticket = db.query(Ticket).filter_by(id=ticket_id).first()
            return ticket.to_dict() if ticket else None
        finally:
            db.close()

    def get_tickets_stats(self):
        """Retorna estatísticas sobre os tickets"""
        db = SessionLocal()
        try:
            total = db.query(Ticket).count()

            # Contar por status
            status_counts = db.query(
                Ticket.status,
                func.count(Ticket.id)
            ).group_by(Ticket.status).all()

            return {
                'total': total,
                'by_status': {status: count for status, count in status_counts}
            }
        finally:
            db.close()


# Instância singleton
ticket_service = TicketService()
