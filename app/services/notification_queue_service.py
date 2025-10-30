# -*- coding: utf-8 -*-
"""
Serviço de Fila de Notificações em Tempo Real

Este módulo fornece uma fila thread-safe para gerenciar notificações Socket.IO.

Arquitetura:
- Threads de processamento pesado (ex: upload de arquivos) adicionam notificações à fila
- Worker eventlet em background processa a fila e emite via Socket.IO
- Garante que notificações sejam entregues em tempo real sem bloquear a aplicação

Exemplo de uso:
    from app.services.notification_queue_service import add_notification

    notification_data = {
        'user_id': 1,
        'title': 'Upload Concluído',
        'message': 'Arquivo processado com sucesso'
    }
    add_notification(notification_data)
"""
import queue

# Fila global thread-safe para notificações pendentes
notification_queue = queue.Queue()


def add_notification(notification_data):
    """
    Adiciona uma notificação à fila para envio em tempo real

    Args:
        notification_data (dict): Dados da notificação incluindo user_id
    """
    notification_queue.put(notification_data)


def get_queue():
    """
    Retorna a instância da fila de notificações

    Returns:
        queue.Queue: Fila thread-safe de notificações
    """
    return notification_queue
