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
    client = client_service.get_client_by_id(client_id)

    if not client:
        return render_template('pages/tickets/list.html', clients=client_service.get_all_clients())

    # Buscar tickets pela organização vinculada
    tickets = []
    if client.get('organization_name'):
        tickets = ticket_service.get_tickets_by_organization(client['organization_name'])

    return render_template('pages/tickets/view.html', client=client, tickets=tickets)


def client_manage(client_id):
    """Tela de gerenciamento de cliente com sidebar de organizações (para rota tickets)"""
    from flask import render_template, redirect, url_for, flash
    from app.models.client_organization import ClientOrganization
    from app.models.organization import Organization
    from app.models.database import db_session

    # Buscar cliente
    client = client_service.get_client_by_id(client_id)

    if not client:
        flash('Cliente não encontrado', 'error')
        return redirect(url_for('admin.tickets_list'))

    # Buscar organizações vinculadas
    organizations = db_session.query(Organization).join(
        ClientOrganization,
        Organization.id == ClientOrganization.organization_id
    ).filter(
        ClientOrganization.client_id == client_id
    ).order_by(Organization.business_name).all()

    organizations_data = [{
        'id': org.id,
        'business_name': org.business_name,
        'person_type': org.person_type
    } for org in organizations]

    return render_template(
        'pages/tickets/manage_client.html',
        client=client,
        organizations=organizations_data
    )
