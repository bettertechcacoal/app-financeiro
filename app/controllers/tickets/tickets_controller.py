# -*- coding: utf-8 -*-
from flask import render_template, request
from app.services.client_service import client_service
from app.services.ticket_service import ticket_service


def tickets_list():
    """Lista de clientes com opção de visualizar tickets"""
    clients = client_service.get_all_clients()
    return render_template('pages/tickets/list.html', clients=clients)


def tickets_view(client_id):
    """Visualiza tickets de um cliente/organização"""
    from app.models.client_organization import ClientOrganization
    from app.models.organization import Organization
    from app.models.database import db_session

    client = client_service.get_client_by_id(client_id)

    if not client:
        return render_template('pages/tickets/list.html', clients=client_service.get_all_clients())

    # Buscar todas as organizações vinculadas ao cliente
    organizations = db_session.query(Organization).join(
        ClientOrganization,
        Organization.id == ClientOrganization.organization_id
    ).filter(
        ClientOrganization.client_id == client_id
    ).order_by(Organization.business_name).all()

    # Buscar tickets para cada organização
    organizations_with_tickets = []
    total_tickets = 0

    for org in organizations:
        tickets = ticket_service.get_tickets_by_organization(org.business_name)
        organizations_with_tickets.append({
            'id': org.id,
            'business_name': org.business_name,
            'person_type': org.person_type,
            'tickets': tickets,
            'tickets_count': len(tickets)
        })
        total_tickets += len(tickets)

    return render_template(
        'pages/tickets/view.html',
        client=client,
        organizations=organizations_with_tickets,
        total_tickets=total_tickets
    )


