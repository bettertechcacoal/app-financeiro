"""
Controller para gerenciar integração com Storage Service
"""
import os
import requests
from flask import jsonify, session, request
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


def get_storage_config():
    """
    Retorna configurações do storage service para o frontend.
    Apenas usuários autenticados podem acessar.

    NOTA: Não retorna mais a API key - o upload será feito via rota intermediária

    Returns:
        JSON com configurações básicas do storage service
    """
    # Verificar se usuário está autenticado
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'message': 'Não autorizado'
        }), 401

    # Obter configurações do .env
    storage_bucket = os.getenv('STORAGE_SERVICE_BUCKET', 'financial-attachments')

    return jsonify({
        'success': True,
        'data': {
            'bucket': storage_bucket,
            'user_id': session.get('user_id'),
            'max_file_size': 5 * 1024 * 1024,  # 5MB em bytes
            'allowed_extensions': ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx', '.xls', '.xlsx']
        }
    })


def get_storage_health():
    """
    Verifica se o storage service está disponível.

    Returns:
        JSON com status do storage service
    """
    import requests

    # Verificar se usuário está autenticado
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'message': 'Não autorizado'
        }), 401

    storage_url = os.getenv('STORAGE_SERVICE_URL', 'http://localhost:8000/api')
    timeout = int(os.getenv('STORAGE_SERVICE_TIMEOUT', 30))

    try:
        # Fazer request para health check do storage service
        response = requests.get(f"{storage_url.replace('/api', '')}/api/health", timeout=5)

        if response.status_code == 200:
            data = response.json()
            return jsonify({
                'success': True,
                'data': {
                    'available': True,
                    'service': data.get('service'),
                    'version': data.get('version'),
                    'status': data.get('status')
                }
            })
        else:
            return jsonify({
                'success': False,
                'data': {
                    'available': False,
                    'message': 'Storage service retornou erro'
                }
            })

    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'data': {
                'available': False,
                'message': 'Timeout ao conectar com storage service'
            }
        })

    except requests.exceptions.ConnectionError:
        return jsonify({
            'success': False,
            'data': {
                'available': False,
                'message': 'Não foi possível conectar ao storage service'
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'data': {
                'available': False,
                'message': f'Erro ao verificar storage service: {str(e)}'
            }
        })


def _check_bucket_exists(storage_url, storage_api_key, storage_bucket, timeout):
    """
    Verifica se o bucket existe no storage service.

    Args:
        storage_url: URL base da API do storage service
        storage_api_key: Chave de autenticação
        storage_bucket: Nome do bucket
        timeout: Timeout das requisições

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        headers = {'Authorization': f'Bearer {storage_api_key}'}

        # Verificar se bucket existe
        check_response = requests.get(
            f'{storage_url}/buckets/{storage_bucket}',
            headers=headers,
            timeout=5
        )

        if check_response.status_code == 200:
            return True, 'Bucket existe'

        # Bucket não existe
        if check_response.status_code == 404:
            return False, f'Bucket "{storage_bucket}" não existe. Crie o bucket no storage-service antes de fazer upload.'

        # Erro de autenticação
        if check_response.status_code == 401:
            return False, 'API Key inválida ou expirada. Verifique STORAGE_SERVICE_API_KEY no .env'

        # Outro erro
        return False, f'Erro ao verificar bucket: HTTP {check_response.status_code}'

    except requests.exceptions.Timeout:
        return False, f'Timeout ao conectar com storage service em {storage_url}'

    except requests.exceptions.ConnectionError:
        return False, f'Não foi possível conectar ao storage service em {storage_url}. Verifique se o serviço está rodando.'

    except Exception as e:
        return False, f'Erro ao verificar bucket: {str(e)}'


def upload_file():
    """
    Rota intermediária para fazer upload de arquivos para o storage service.
    Recebe o arquivo do frontend e envia para o storage service com a API key segura.

    Expected form-data:
        - file: arquivo a ser enviado
        - expense_type: tipo da despesa (vehicle, lodging, other)
        - expense_id: ID da despesa
        - payout_id: ID do repasse

    Returns:
        JSON com informações do arquivo armazenado
    """
    # Verificar se usuário está autenticado
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'message': 'Não autorizado'
        }), 401

    # Verificar se arquivo foi enviado
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'message': 'Nenhum arquivo foi enviado'
        }), 400

    file = request.files['file']

    # Verificar se arquivo tem nome
    if file.filename == '':
        return jsonify({
            'success': False,
            'message': 'Arquivo sem nome'
        }), 400

    # Obter metadados
    expense_type = request.form.get('expense_type', '')
    expense_id = request.form.get('expense_id', '')
    payout_id = request.form.get('payout_id', '')

    # Validar metadados obrigatórios
    if not expense_type or not expense_id or not payout_id:
        return jsonify({
            'success': False,
            'message': 'Metadados incompletos (expense_type, expense_id, payout_id são obrigatórios)'
        }), 400

    # Obter configurações do storage service
    storage_url = os.getenv('STORAGE_SERVICE_URL', 'http://localhost:8000/api')
    storage_api_key = os.getenv('STORAGE_SERVICE_API_KEY', '')
    storage_bucket = os.getenv('STORAGE_SERVICE_BUCKET', 'financial-attachments')
    timeout = int(os.getenv('STORAGE_SERVICE_TIMEOUT', 30))

    # Validar se API key está configurada
    if not storage_api_key:
        return jsonify({
            'success': False,
            'message': 'Storage service não configurado no servidor'
        }), 500

    # Verificar se o bucket existe
    bucket_ok, bucket_msg = _check_bucket_exists(storage_url, storage_api_key, storage_bucket, timeout)
    if not bucket_ok:
        return jsonify({
            'success': False,
            'message': bucket_msg
        }), 400

    try:
        # Preparar metadados como campos individuais no FormData
        # O Laravel espera metadata como array, então enviamos como metadata[key]
        # NOTA: Não enviamos 'path' pois o storage-service agora usa estrutura WordPress (ano/mes/dia)
        data = {
            'metadata[expense_type]': expense_type,
            'metadata[expense_id]': expense_id,
            'metadata[payout_id]': payout_id,
            'metadata[uploaded_by]': str(session.get('user_id')),
            'uploader_uuid': f"user_{session.get('user_id')}"
        }

        # Preparar arquivo para envio
        files = {
            'file': (file.filename, file.stream, file.content_type)
        }

        headers = {
            'Authorization': f'Bearer {storage_api_key}'
        }

        # Fazer upload para o storage service
        response = requests.post(
            f'{storage_url}/buckets/{storage_bucket}/files',
            files=files,
            data=data,
            headers=headers,
            timeout=timeout
        )

        # Verificar resposta
        if response.status_code == 201:
            result = response.json()
            if result.get('success'):
                # Retornar dados do arquivo
                return jsonify({
                    'success': True,
                    'data': result['data'],
                    'message': 'Arquivo enviado com sucesso'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': result.get('message', 'Erro desconhecido no storage service')
                }), 500
        else:
            # Tentar obter mensagem de erro detalhada
            try:
                error_data = response.json()
                error_message = error_data.get('message', 'Erro ao enviar arquivo')

                # Se houver erros de validação, incluir
                if 'errors' in error_data:
                    errors_detail = error_data['errors']
                    error_message = f"{error_message}. Detalhes: {errors_detail}"

            except:
                error_message = f'Erro HTTP {response.status_code}'
                try:
                    # Tentar obter o texto da resposta
                    error_message += f'. Resposta: {response.text[:200]}'
                except:
                    pass

            return jsonify({
                'success': False,
                'message': error_message,
                'status_code': response.status_code
            }), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'message': 'Timeout ao conectar com storage service'
        }), 504

    except requests.exceptions.ConnectionError:
        return jsonify({
            'success': False,
            'message': 'Não foi possível conectar ao storage service'
        }), 503

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao processar upload: {str(e)}'
        }), 500


def delete_file(file_uuid):
    """
    Rota intermediária para deletar arquivos do storage service.
    Proxy para o storage service mantendo a API key segura.

    Args:
        file_uuid: UUID do arquivo no storage service

    Returns:
        JSON com resultado da operação
    """
    # Verificar se usuário está autenticado
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'message': 'Não autorizado'
        }), 401

    # Obter configurações do storage service
    storage_url = os.getenv('STORAGE_SERVICE_URL', 'http://localhost:8000/api')
    storage_api_key = os.getenv('STORAGE_SERVICE_API_KEY', '')
    timeout = int(os.getenv('STORAGE_SERVICE_TIMEOUT', 30))

    # Validar se API key está configurada
    if not storage_api_key:
        return jsonify({
            'success': False,
            'message': 'Storage service não configurado no servidor'
        }), 500

    try:
        headers = {
            'Authorization': f'Bearer {storage_api_key}'
        }

        # Fazer request de delete para o storage service
        response = requests.delete(
            f'{storage_url}/files/{file_uuid}',
            headers=headers,
            timeout=timeout
        )

        # Verificar resposta
        if response.status_code == 200:
            try:
                result = response.json()
                return jsonify({
                    'success': True,
                    'message': result.get('message', 'Arquivo deletado com sucesso')
                })
            except:
                return jsonify({
                    'success': True,
                    'message': 'Arquivo deletado com sucesso'
                })
        else:
            # Tentar obter mensagem de erro
            try:
                error_data = response.json()
                error_message = error_data.get('message', 'Erro ao deletar arquivo')
            except:
                error_message = f'Erro HTTP {response.status_code}'

            return jsonify({
                'success': False,
                'message': error_message
            }), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'message': 'Timeout ao conectar com storage service'
        }), 504

    except requests.exceptions.ConnectionError:
        return jsonify({
            'success': False,
            'message': 'Não foi possível conectar ao storage service'
        }), 503

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao processar deleção: {str(e)}'
        }), 500


def download_file(file_uuid):
    """
    Rota intermediária para fazer download de arquivos do storage service.
    Proxy para o storage service mantendo a API key segura.

    Args:
        file_uuid: UUID do arquivo no storage service

    Returns:
        Arquivo ou JSON com erro
    """
    # Verificar se usuário está autenticado
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'message': 'Não autorizado'
        }), 401

    # Obter configurações do storage service
    storage_url = os.getenv('STORAGE_SERVICE_URL', 'http://localhost:8000/api')
    storage_api_key = os.getenv('STORAGE_SERVICE_API_KEY', '')
    timeout = int(os.getenv('STORAGE_SERVICE_TIMEOUT', 30))

    # Validar se API key está configurada
    if not storage_api_key:
        return jsonify({
            'success': False,
            'message': 'Storage service não configurado no servidor'
        }), 500

    try:
        headers = {
            'Authorization': f'Bearer {storage_api_key}'
        }

        # Fazer request para o storage service
        response = requests.get(
            f'{storage_url}/files/{file_uuid}/download',
            headers=headers,
            timeout=timeout,
            stream=True
        )

        # Verificar resposta
        if response.status_code == 200:
            # Retornar o arquivo como proxy
            from flask import Response
            return Response(
                response.iter_content(chunk_size=8192),
                content_type=response.headers.get('Content-Type', 'application/octet-stream'),
                headers={
                    'Content-Disposition': response.headers.get('Content-Disposition', 'attachment')
                }
            )
        else:
            # Tentar obter mensagem de erro
            try:
                error_data = response.json()
                error_message = error_data.get('message', 'Erro ao baixar arquivo')
            except:
                error_message = f'Erro HTTP {response.status_code}'

            return jsonify({
                'success': False,
                'message': error_message
            }), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'message': 'Timeout ao conectar com storage service'
        }), 504

    except requests.exceptions.ConnectionError:
        return jsonify({
            'success': False,
            'message': 'Não foi possível conectar ao storage service'
        }), 503

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao processar download: {str(e)}'
        }), 500
