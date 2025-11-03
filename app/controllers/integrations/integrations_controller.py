# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, jsonify
from app.services.movidesk_service import movidesk_service


def integrations_list():
    """Lista todas as integrações disponíveis"""
    integrations = [
        {
            'id': 'movidesk',
            'name': 'Movidesk',
            'description': 'Sistema de helpdesk e gestão de tickets',
            'icon': 'fa-headset',
            'color': 'blue'
        },
        {
            'id': 'whatsapp',
            'name': 'WhatsApp',
            'description': 'Integração com WhatsApp via Evolution API',
            'icon': 'fa-whatsapp',
            'color': 'green'
        }
    ]
    return render_template('pages/integrations/list.html', integrations=integrations)


def movidesk_options():
    """Exibe opções de integração do Movidesk"""
    options = [
        {
            'id': 'tickets',
            'name': 'Tickets',
            'description': 'Sincronize tickets de atendimento',
            'icon': 'fa-ticket-alt',
            'color': 'green',
            'route': 'admin.movidesk_tickets'
        },
        {
            'id': 'organizations',
            'name': 'Organizações',
            'description': 'Sincronize organizações do Movidesk',
            'icon': 'fa-building',
            'color': 'purple',
            'route': 'admin.movidesk_organizations'
        }
    ]
    return render_template('pages/integrations/movidesk_options.html', options=options)


def movidesk_organizations():
    """Tela de sincronização de organizações"""
    from app.models.organization import Organization
    from app.models.client import Client
    from app.models.client_organization import ClientOrganization
    from app.models.database import db_session
    from sqlalchemy import or_, func, select

    # Parâmetros de pesquisa e paginação
    search = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 20

    # Subquery para contar clientes vinculados a cada organização
    clients_count_subquery = (
        select(
            ClientOrganization.organization_id,
            func.count(ClientOrganization.client_id).label('clients_count')
        )
        .group_by(ClientOrganization.organization_id)
        .subquery()
    )

    # Query principal com LEFT JOIN na subquery
    query = db_session.query(
        Organization,
        func.coalesce(clients_count_subquery.c.clients_count, 0).label('clients_count')
    ).outerjoin(
        clients_count_subquery,
        Organization.id == clients_count_subquery.c.organization_id
    )

    # Aplicar filtro de pesquisa
    if search:
        query = query.filter(
            or_(
                Organization.business_name.ilike(f'%{search}%'),
                Organization.id.ilike(f'%{search}%')
            )
        )

    # Ordenar por nome
    query = query.order_by(Organization.business_name)

    # Contar total
    total = query.count()
    total_pages = (total + per_page - 1) // per_page

    # Aplicar paginação
    offset = (page - 1) * per_page
    results = query.limit(per_page).offset(offset).all()

    # Preparar dados para o template
    organizations = []
    for org, clients_count in results:
        organizations.append({
            'id': org.id,
            'business_name': org.business_name,
            'person_type': org.person_type,
            'cnpj': None,  # Adicionar se tiver o campo no modelo
            'clients_count': clients_count
        })

    # Buscar estatísticas
    stats = movidesk_service.get_organizations_stats()

    return render_template(
        'pages/integrations/movidesk_organizations.html',
        stats=stats,
        organizations=organizations,
        page=page,
        total_pages=total_pages,
        search=search
    )


def movidesk_sync_organizations():
    """API para sincronizar organizações"""
    try:
        result = movidesk_service.sync_organizations()
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def organization_edit(org_id):
    """Tela de edição de organização"""
    from app.models.organization import Organization
    from app.models.client import Client
    from app.models.client_organization import ClientOrganization
    from app.models.database import db_session

    # Buscar organização
    organization = db_session.query(Organization).filter_by(id=org_id).first()

    if not organization:
        flash('Organização não encontrada', 'error')
        return redirect(url_for('admin.movidesk_organizations'))

    # Buscar clientes vinculados através da tabela de associação
    clients = db_session.query(Client).join(
        ClientOrganization,
        Client.id == ClientOrganization.client_id
    ).filter(
        ClientOrganization.organization_id == org_id
    ).order_by(Client.name).all()

    return render_template(
        'pages/integrations/organization_edit.html',
        organization=organization,
        clients=clients
    )


def organization_update(org_id):
    """Atualiza dados da organização"""
    from app.models.organization import Organization
    from app.models.database import db_session

    organization = db_session.query(Organization).filter_by(id=org_id).first()

    if not organization:
        flash('Organização não encontrada', 'error')
        return redirect(url_for('admin.movidesk_organizations'))

    try:
        # Atualizar campos
        organization.business_name = request.form.get('business_name')
        organization.person_type = request.form.get('person_type')

        db_session.commit()
        flash('Organização atualizada com sucesso!', 'success')
    except Exception as e:
        db_session.rollback()
        flash(f'Erro ao atualizar organização: {str(e)}', 'error')

    return redirect(url_for('admin.organization_edit', org_id=org_id))


def movidesk_tickets():
    """Tela de sincronização de tickets"""
    stats = movidesk_service.get_tickets_stats()
    return render_template('pages/integrations/movidesk_tickets.html', stats=stats)


def movidesk_sync_tickets():
    """API para sincronizar tickets"""
    try:
        data = request.get_json()
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if not start_date or not end_date:
            return jsonify({'success': False, 'error': 'Datas obrigatórias'}), 400

        result = movidesk_service.sync_tickets(start_date, end_date)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def get_unlinked_clients():
    """API para obter clientes sem organização vinculada"""
    from app.models.client import Client
    from app.models.client_organization import ClientOrganization
    from app.models.database import db_session
    from sqlalchemy import select

    try:
        # Subquery para obter IDs de clientes que já possuem vínculo
        linked_clients_subquery = (
            select(ClientOrganization.client_id)
            .distinct()
            .subquery()
        )

        # Buscar clientes que não estão vinculados a nenhuma organização
        clients = db_session.query(Client).filter(
            ~Client.id.in_(select(linked_clients_subquery))
        ).order_by(Client.name).all()

        clients_data = [{
            'id': client.id,
            'name': client.name,
            'email': client.email,
            'document': client.document,
            'phone': client.phone
        } for client in clients]

        return jsonify({'success': True, 'clients': clients_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def link_client_to_organization(org_id, client_id):
    """API para vincular cliente à organização"""
    from app.models.organization import Organization
    from app.models.client import Client
    from app.models.client_organization import ClientOrganization
    from app.models.database import db_session

    try:
        # Verificar se organização existe
        organization = db_session.query(Organization).filter_by(id=org_id).first()
        if not organization:
            return jsonify({'success': False, 'error': 'Organização não encontrada'}), 404

        # Verificar se cliente existe
        client = db_session.query(Client).filter_by(id=client_id).first()
        if not client:
            return jsonify({'success': False, 'error': 'Cliente não encontrado'}), 404

        # Verificar se já existe vinculação
        existing = db_session.query(ClientOrganization).filter_by(
            client_id=client_id,
            organization_id=org_id
        ).first()

        if existing:
            return jsonify({'success': False, 'error': 'Cliente já está vinculado a esta organização'}), 400

        # Criar vinculação
        client_org = ClientOrganization(
            client_id=client_id,
            organization_id=org_id
        )
        db_session.add(client_org)
        db_session.commit()

        return jsonify({'success': True, 'message': 'Cliente vinculado com sucesso'})
    except Exception as e:
        db_session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


def unlink_client_from_organization(org_id, client_id):
    """API para desvincular cliente da organização"""
    from app.models.client_organization import ClientOrganization
    from app.models.database import db_session

    try:
        # Verificar se existe vinculação
        client_org = db_session.query(ClientOrganization).filter_by(
            client_id=client_id,
            organization_id=org_id
        ).first()

        if not client_org:
            return jsonify({'success': False, 'error': 'Cliente não está vinculado a esta organização'}), 404

        # Remover vinculação
        db_session.delete(client_org)
        db_session.commit()

        return jsonify({'success': True, 'message': 'Cliente desvinculado com sucesso'})
    except Exception as e:
        db_session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


def toggle_organization_status(org_id):
    """API para ativar/inativar organização"""
    from app.models.organization import Organization
    from app.models.database import db_session

    try:
        # Buscar organização
        organization = db_session.query(Organization).filter_by(id=org_id).first()
        if not organization:
            return jsonify({'success': False, 'error': 'Organização não encontrada'}), 404

        # Obter novo status
        data = request.get_json()
        is_active = data.get('is_active', True)

        # Atualizar status
        organization.is_active = is_active
        db_session.commit()

        action = 'ativada' if is_active else 'inativada'
        return jsonify({'success': True, 'message': f'Organização {action} com sucesso'})
    except Exception as e:
        db_session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
