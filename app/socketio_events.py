# -*- coding: utf-8 -*-
from flask_socketio import emit, join_room, leave_room
from flask import session
from app.models.notification import Notification
from app.models.database import get_db


def register_socketio_events(socketio):
    """Registra todos os eventos Socket.IO"""

    @socketio.on('connect')
    def handle_connect():
        """Quando um cliente se conecta"""
        user_id = session.get('user_id')
        if user_id:
            # Adicionar o usuário a uma sala específica (room) baseada em seu ID
            join_room(f'user_{user_id}')
            emit('connected', {'message': 'Conectado ao servidor de notificações'})
        else:
            return False  # Rejeitar conexão não autenticada

    @socketio.on('disconnect')
    def handle_disconnect():
        """Quando um cliente se desconecta"""
        user_id = session.get('user_id')
        if user_id:
            leave_room(f'user_{user_id}')

    @socketio.on('request_notifications')
    def handle_request_notifications(data):
        """Quando o cliente solicita notificações"""
        user_id = session.get('user_id')
        if not user_id:
            emit('error', {'message': 'Não autenticado'})
            return

        db = get_db()
        try:
            # Buscar últimas notificações
            limit = data.get('limit', 10)
            notifications = db.query(Notification).filter_by(
                user_id=user_id
            ).order_by(Notification.created_at.desc()).limit(limit).all()

            # Contar não lidas
            unread_count = db.query(Notification).filter_by(
                user_id=user_id,
                is_read=False
            ).count()

            emit('notifications_update', {
                'notifications': [n.to_dict() for n in notifications],
                'unread_count': unread_count
            })
        except Exception as e:
            emit('error', {'message': str(e)})

    @socketio.on('mark_as_read')
    def handle_mark_as_read(data):
        """Marca uma notificação como lida"""
        user_id = session.get('user_id')
        if not user_id:
            emit('error', {'message': 'Não autenticado'})
            return

        notification_id = data.get('notification_id')
        if not notification_id:
            emit('error', {'message': 'ID da notificação não fornecido'})
            return

        db = get_db()
        try:
            from datetime import datetime
            notification = db.query(Notification).filter_by(
                id=notification_id,
                user_id=user_id
            ).first()

            if notification:
                notification.is_read = True
                notification.read_at = datetime.now()
                db.commit()

                # Contar não lidas restantes
                unread_count = db.query(Notification).filter_by(
                    user_id=user_id,
                    is_read=False
                ).count()

                emit('notification_marked_read', {
                    'notification_id': notification_id,
                    'unread_count': unread_count
                })
            else:
                emit('error', {'message': 'Notificação não encontrada'})
        except Exception as e:
            db.rollback()
            emit('error', {'message': str(e)})


def send_notification_to_user(socketio, user_id, notification):
    """
    Função auxiliar para enviar notificação em tempo real para um usuário específico
    Pode ser chamada de qualquer lugar do código
    """
    try:
        socketio.emit(
            'new_notification',
            notification.to_dict(),
            room=f'user_{user_id}'
        )
    except Exception as e:
        pass  # Silenciar erros de notificação em tempo real
