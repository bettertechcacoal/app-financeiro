# -*- coding: utf-8 -*-
import requests
from typing import Optional

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
        api_url = 'http://localhost:8080'
        api_key = 'change-me-to-secure-key'

        print(f"[WHATSAPP] Tentando enviar para: {phone_number}")
        print(f"[WHATSAPP] Instância fornecida: {instance_name}")

        # Se não foi especificada instância, busca a primeira disponível
        if not instance_name:
            print(f"[WHATSAPP] Buscando instâncias disponíveis...")
            response = requests.get(
                f'{api_url}/instance/fetchInstances',
                headers={'apikey': api_key},
                timeout=5
            )

            print(f"[WHATSAPP] Status da busca de instâncias: {response.status_code}")

            if response.status_code == 200:
                instances = response.json()
                print(f"[WHATSAPP] Instâncias encontradas: {instances}")
                if not instances:
                    print(f"[WHATSAPP] Nenhuma instância disponível")
                    return False

                # Pegar primeira instância disponível
                first_instance = instances[0] if isinstance(instances, list) else list(instances.values())[0]
                # Tentar múltiplos campos possíveis para o nome da instância
                instance_name = (first_instance.get('name') or
                               first_instance.get('instanceName') or
                               first_instance.get('instance', {}).get('instanceName') or
                               first_instance.get('instance', {}).get('name'))
                print(f"[WHATSAPP] Instância selecionada: {instance_name}")

                if not instance_name:
                    print(f"[WHATSAPP] Nome da instância não encontrado")
                    return False
            else:
                print(f"[WHATSAPP] Erro ao buscar instâncias: {response.status_code}")
                return False

        # Enviar mensagem
        print(f"[WHATSAPP] Enviando mensagem para {phone_number} via instância {instance_name}")
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

        print(f"[WHATSAPP] Status do envio: {response.status_code}")
        print(f"[WHATSAPP] Resposta: {response.text}")

        return response.status_code == 201 or response.status_code == 200

    except Exception as e:
        print(f"[WHATSAPP] Erro ao enviar WhatsApp: {e}")
        import traceback
        print(f"[WHATSAPP] Traceback: {traceback.format_exc()}")
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

    print(f"[WHATSAPP] Telefone limpo: {clean_phone} (tamanho: {len(clean_phone)})")

    # Se não tem código do país (10 ou 11 dígitos), adiciona 55 (Brasil)
    if len(clean_phone) == 11 or len(clean_phone) == 10:
        clean_phone = '55' + clean_phone
        print(f"[WHATSAPP] Adicionado código do país: {clean_phone}")

    # Validar tamanho mínimo
    if len(clean_phone) < 12:
        print(f"[WHATSAPP] Telefone inválido - tamanho menor que 12: {len(clean_phone)}")
        return None

    print(f"[WHATSAPP] Telefone final formatado: {clean_phone}")
    return clean_phone
