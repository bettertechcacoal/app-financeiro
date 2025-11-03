# -*- coding: utf-8 -*-
"""
Controller para API do WhatsApp (Evolution API)
Todas as requisições para Evolution API passam por aqui, protegendo a API Key
"""
from flask import jsonify, request, render_template
from config import app as app_config
import requests


def evolution_whatsapp_options():
    """Exibe página de gerenciamento do WhatsApp"""
    # Não passa a API Key para o template, apenas a URL
    return render_template(
        'pages/integrations/whatsapp_options.html',
        evolution_api_url=app_config.EVOLUTION_API_URL
    )


def evolution_fetch_instances():
    """
    GET /admin/api/whatsapp/instances
    Lista todas as instâncias WhatsApp
    """
    try:
        response = requests.get(
            f'{app_config.EVOLUTION_API_URL}/instance/fetchInstances',
            headers={'apikey': app_config.EVOLUTION_API_KEY},
            timeout=10
        )

        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({'error': 'Erro ao buscar instâncias', 'details': response.text}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Erro ao conectar com Evolution API', 'details': str(e)}), 500


def evolution_create_instance():
    """
    POST /admin/api/whatsapp/instances
    Cria uma nova instância WhatsApp
    Body: { "instanceName": "nome-da-instancia" }
    """
    try:
        data = request.get_json()
        instance_name = data.get('instanceName')

        if not instance_name:
            return jsonify({'error': 'Nome da instância é obrigatório'}), 400

        response = requests.post(
            f'{app_config.EVOLUTION_API_URL}/instance/create',
            headers={
                'apikey': app_config.EVOLUTION_API_KEY,
                'Content-Type': 'application/json'
            },
            json={
                'instanceName': instance_name,
                'integration': 'WHATSAPP-BAILEYS',
                'qrcode': True
            },
            timeout=10
        )

        if response.status_code in [200, 201]:
            return jsonify(response.json()), response.status_code
        else:
            return jsonify({'error': 'Erro ao criar instância', 'details': response.text}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Erro ao conectar com Evolution API', 'details': str(e)}), 500


def evolution_connection_state(instance_name):
    """
    GET /admin/api/whatsapp/instances/<instance_name>/connection-state
    Verifica estado de conexão da instância
    """
    try:
        response = requests.get(
            f'{app_config.EVOLUTION_API_URL}/instance/connectionState/{instance_name}',
            headers={'apikey': app_config.EVOLUTION_API_KEY},
            timeout=10
        )

        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({'error': 'Erro ao verificar estado', 'details': response.text}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Erro ao conectar com Evolution API', 'details': str(e)}), 500


def evolution_send_message(instance_name):
    """
    POST /admin/api/whatsapp/instances/<instance_name>/send-message
    Envia mensagem de texto via WhatsApp
    Body: { "number": "5569999999999", "text": "Mensagem" }
    """
    try:
        data = request.get_json()
        phone_number = data.get('number')
        message = data.get('text')

        if not phone_number or not message:
            return jsonify({'error': 'Número e mensagem são obrigatórios'}), 400

        response = requests.post(
            f'{app_config.EVOLUTION_API_URL}/message/sendText/{instance_name}',
            headers={
                'apikey': app_config.EVOLUTION_API_KEY,
                'Content-Type': 'application/json'
            },
            json={
                'number': phone_number,
                'text': message
            },
            timeout=10
        )

        if response.status_code in [200, 201]:
            return jsonify(response.json()), response.status_code
        else:
            return jsonify({'error': 'Erro ao enviar mensagem', 'details': response.text}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Erro ao conectar com Evolution API', 'details': str(e)}), 500


def evolution_delete_instance(instance_name):
    """
    DELETE /admin/api/whatsapp/instances/<instance_name>
    Deleta uma instância WhatsApp
    """
    try:
        response = requests.delete(
            f'{app_config.EVOLUTION_API_URL}/instance/delete/{instance_name}',
            headers={'apikey': app_config.EVOLUTION_API_KEY},
            timeout=10
        )

        if response.status_code in [200, 204]:
            return jsonify({'message': 'Instância deletada com sucesso'}), 200
        else:
            return jsonify({'error': 'Erro ao deletar instância', 'details': response.text}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Erro ao conectar com Evolution API', 'details': str(e)}), 500


def evolution_check_api_status():
    """
    GET /admin/api/whatsapp/status
    Verifica se a Evolution API está online
    """
    try:
        response = requests.get(
            app_config.EVOLUTION_API_URL,
            timeout=5
        )

        return jsonify({'status': 'online'}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'offline', 'error': str(e)}), 503
