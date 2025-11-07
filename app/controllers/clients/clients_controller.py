# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, jsonify
from app.services.client_service import client_service


def clients_list():
    """Lista de clientes"""
    clients = client_service.get_all_clients()
    return render_template('pages/clients/manage.html', clients=clients)


def client_new():
    """Formulário de novo cliente"""
    return render_template('pages/clients/form.html', client=None)


def client_create():
    """Cria um novo cliente"""
    try:
        # Validação dos campos obrigatórios
        name = request.form.get('name', '').strip()
        document = request.form.get('document', '').strip()
        billing_cycle_type = request.form.get('billing_cycle_type', '').strip()

        errors = []

        if not name:
            errors.append('O campo "Nome / Razão Social" é obrigatório')

        if not document:
            errors.append('O campo "CNPJ / CPF" é obrigatório')

        if not billing_cycle_type:
            errors.append('O campo "Tipo de Ciclo" é obrigatório')

        # Se o tipo de ciclo for "fixo", validar dia de início
        if billing_cycle_type == 'fixo':
            fixed_start_day = request.form.get('fixed_start_day', '').strip()
            if not fixed_start_day:
                errors.append('Para ciclo fixo, o campo "Dia de Início" é obrigatório')

        # Se houver erros de validação, retornar ao formulário com mensagens
        if errors:
            for error in errors:
                flash(error, 'error')
            # Retornar para o formulário mantendo os dados preenchidos
            return render_template('pages/clients/form.html', client=None, form_data=request.form)

        client_data = {
            'name': name,
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'document': document,
            'address': request.form.get('address'),
            'city': request.form.get('city'),
            'state': request.form.get('state'),
            'zipcode': request.form.get('zipcode'),
            'billing_cycle': request.form.get('billing_cycle'),
            'billing_day': request.form.get('billing_day'),
            'billing_cycle_type': billing_cycle_type,
            'fixed_start_day': request.form.get('fixed_start_day') if billing_cycle_type == 'fixo' else None
        }

        client = client_service.create_client(client_data)

        # Salvar meta dados do contrato
        meta_data = {}
        if request.form.get('contract_number'):
            meta_data['contract_number'] = request.form.get('contract_number')
        if request.form.get('contract_year'):
            meta_data['contract_year'] = request.form.get('contract_year')
        if request.form.get('process_number'):
            meta_data['process_number'] = request.form.get('process_number')
        if request.form.get('process_year'):
            meta_data['process_year'] = request.form.get('process_year')

        if meta_data:
            client_service.update_client_metas(client['id'], meta_data)

        flash('Organização cadastrada com sucesso!', 'success')
        return redirect(url_for('admin.client_edit', client_id=client['id']))
    except Exception as e:
        flash(f'Erro ao cadastrar organização: {str(e)}', 'error')
        # Retornar para o formulário mantendo os dados preenchidos
        return render_template('pages/clients/form.html', client=None, form_data=request.form)


def client_edit(client_id):
    """Exibe formulário de edição de cliente"""
    client = client_service.get_client_by_id(client_id)
    if not client:
        flash('Organização não encontrada', 'error')
        return redirect(url_for('admin.clients_list'))

    # Carregar aplicações do cliente
    client_applications = client_service.get_client_applications(client_id)

    return render_template('pages/clients/form.html', client=client, client_applications=client_applications)


def client_update(client_id):
    """Atualiza um cliente"""
    try:
        # Validação dos campos obrigatórios
        name = request.form.get('name', '').strip()
        document = request.form.get('document', '').strip()
        billing_cycle_type = request.form.get('billing_cycle_type', '').strip()

        errors = []

        if not name:
            errors.append('O campo "Nome / Razão Social" é obrigatório')

        if not document:
            errors.append('O campo "CNPJ / CPF" é obrigatório')

        if not billing_cycle_type:
            errors.append('O campo "Tipo de Ciclo" é obrigatório')

        # Se o tipo de ciclo for "fixo", validar dia de início
        if billing_cycle_type == 'fixo':
            fixed_start_day = request.form.get('fixed_start_day', '').strip()
            if not fixed_start_day:
                errors.append('Para ciclo fixo, o campo "Dia de Início" é obrigatório')

        # Se houver erros de validação, retornar ao formulário com mensagens
        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('admin.client_edit', client_id=client_id))

        client_data = {
            'name': name,
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'document': document,
            'address': request.form.get('address'),
            'city': request.form.get('city'),
            'state': request.form.get('state'),
            'zipcode': request.form.get('zipcode'),
            'billing_cycle': request.form.get('billing_cycle'),
            'billing_day': request.form.get('billing_day'),
            'billing_cycle_type': billing_cycle_type,
            'fixed_start_day': request.form.get('fixed_start_day') if billing_cycle_type == 'fixo' else None
        }

        client = client_service.update_client(client_id, client_data)
        if client:
            # Salvar meta dados do contrato
            meta_data = {}
            if request.form.get('contract_number'):
                meta_data['contract_number'] = request.form.get('contract_number')
            if request.form.get('contract_year'):
                meta_data['contract_year'] = request.form.get('contract_year')
            if request.form.get('process_number'):
                meta_data['process_number'] = request.form.get('process_number')
            if request.form.get('process_year'):
                meta_data['process_year'] = request.form.get('process_year')

            if meta_data:
                client_service.update_client_metas(client_id, meta_data)

            flash('Organização atualizada com sucesso!', 'success')
        else:
            flash('Organização não encontrada', 'error')

        return redirect(url_for('admin.client_edit', client_id=client_id))
    except Exception as e:
        flash(f'Erro ao atualizar organização: {str(e)}', 'error')
        return redirect(url_for('admin.client_edit', client_id=client_id))


def client_delete(client_id):
    """Remove um cliente"""
    try:
        if client_service.delete_client(client_id):
            flash('Organização removida com sucesso!', 'success')
        else:
            flash('Organização não encontrada', 'error')

        return redirect(url_for('admin.clients_list'))
    except Exception as e:
        flash(f'Erro ao remover organização: {str(e)}', 'error')
        return redirect(url_for('admin.clients_list'))


def get_organizations_api():
    """API para buscar organizações"""
    try:
        organizations = client_service.get_organizations()
        return jsonify(organizations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_clients_api():
    """API para buscar todos os clientes"""
    try:
        clients = client_service.get_all_clients()
        # client_service.get_all_clients() já retorna uma lista de dicionários
        return jsonify({'success': True, 'clients': clients})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def get_all_applications_api():
    """API para buscar todas as aplicações disponíveis"""
    try:
        applications = client_service.get_all_applications()
        return jsonify({'success': True, 'applications': applications})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def get_applications_for_client_api(client_id):
    """API para buscar todas as aplicações com flag indicando se estão vinculadas ao cliente"""
    try:
        applications = client_service.get_applications_for_client(client_id)
        return jsonify({'success': True, 'applications': applications})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def add_application_to_client_api(client_id):
    """API para adicionar uma aplicação ao cliente"""
    try:
        data = request.get_json()
        application_id = data.get('application_id')
        cod_elotech = data.get('cod_elotech')

        if not application_id:
            return jsonify({'success': False, 'error': 'ID da aplicação é obrigatório'}), 400

        result = client_service.add_application_to_client(client_id, application_id, cod_elotech)
        return jsonify({'success': True, 'data': result})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def remove_application_from_client_api(client_id):
    """API para remover uma aplicação do cliente"""
    try:
        data = request.get_json()
        application_id = data.get('application_id')

        if not application_id:
            return jsonify({'success': False, 'error': 'ID da aplicação é obrigatório'}), 400

        client_service.remove_application_from_client(client_id, application_id)
        return jsonify({'success': True})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
