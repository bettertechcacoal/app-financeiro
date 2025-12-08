# -*- coding: utf-8 -*-
import logging
import requests
from typing import Optional
from config import app as app_config

def send_whatsapp_message(phone_number: str, message: str, instance_name: Optional[str] = None) -> bool:
    """
    Envia mensagem via WhatsApp usando Evolution API

    Args:
        phone_number: Número de telefone no formato internacional (ex: 5569999999999)
        message: Texto da mensagem a ser enviada
        instance_name: Nome da instância (se None, pega a primeira disponível)

    Returns:
        bool: True se enviado com sucesso, False caso contrário
    """
    try:
        api_url = app_config.EVOLUTION_API_URL
        api_key = app_config.EVOLUTION_API_KEY

        # Se não foi especificada instância, busca a primeira disponível
        if not instance_name:
            response = requests.get(
                f'{api_url}/instance/fetchInstances',
                headers={'apikey': api_key},
                timeout=5
            )

            if response.status_code == 200:
                instances = response.json()
                if not instances:
                    logging.warning("WhatsApp: Nenhuma instância disponível")
                    return False

                # Pegar primeira instância disponível
                first_instance = instances[0] if isinstance(instances, list) else list(instances.values())[0]
                # Tentar múltiplos campos possíveis para o nome da instância
                instance_name = (first_instance.get('name') or
                               first_instance.get('instanceName') or
                               first_instance.get('instance', {}).get('instanceName') or
                               first_instance.get('instance', {}).get('name'))

                if not instance_name:
                    logging.warning("WhatsApp: Nome da instância não encontrado")
                    return False
            else:
                logging.error(f"WhatsApp: Erro ao buscar instâncias: {response.status_code}")
                return False

        # Enviar mensagem
        response = requests.post(
            f'{api_url}/message/sendText/{instance_name}',
            headers={
                'apikey': api_key,
                'Content-Type': 'application/json'
            },
            json={
                'number': phone_number,
                'text': message
            },
            timeout=10
        )

        if response.status_code in [200, 201]:
            return True
        else:
            logging.error(f"WhatsApp: Erro ao enviar mensagem: {response.status_code}")
            return False

    except Exception as e:
        logging.error(f"WhatsApp: Erro ao enviar mensagem")
        return False


def format_phone_number(phone: str) -> Optional[str]:
    """
    Formata número de telefone para padrão internacional
    Sempre adiciona código 55 (Brasil) se não tiver código de país

    Args:
        phone: Número de telefone em qualquer formato

    Returns:
        str: Número formatado (ex: 5569999999999) ou None se inválido
    """
    if not phone:
        return None

    # Remove todos os caracteres não numéricos
    clean_phone = ''.join(filter(str.isdigit, phone))

    # Se não tem código do país (10 ou 11 dígitos), adiciona 55 (Brasil)
    if len(clean_phone) == 11 or len(clean_phone) == 10:
        clean_phone = '55' + clean_phone

    # Validar tamanho mínimo
    if len(clean_phone) < 12:
        return None

    return clean_phone
