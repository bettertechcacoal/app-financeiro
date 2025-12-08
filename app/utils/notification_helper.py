# -*- coding: utf-8 -*-
"""
Helper para enviar notificações em tempo real

Uso:
    from app.utils.notification_helper import send_notification

    send_notification(
        user_id=1,
        title="Viagem Aprovada",
        message="Sua viagem para Porto Velho foi aprovada",
        notification_type=NotificationType.TRAVEL,
        action_url="/admin/travels/123",
        action_text="Ver Viagem"
    )
"""
import logging

from app.models.notification import Notification, NotificationType
from app.models.database import get_db


def send_notification(user_id, title, message, notification_type=NotificationType.INFO,
                     action_url=None, action_text=None):
    """
    Cria e envia uma notificação em tempo real para um usuário

    Args:
        user_id: ID do usuário que receberá a notificação
        title: Título da notificação
        message: Mensagem da notificação
        notification_type: Tipo da notificação (NotificationType)
        action_url: URL para ação (opcional)
        action_text: Texto do botão de ação (opcional)

    Returns:
        Notification: Objeto da notificação criada
    """
    db = get_db()

    try:
        # Criar notificação no banco
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            action_url=action_url,
            action_text=action_text,
            is_read=False
        )

        db.add(notification)
        db.commit()
        db.refresh(notification)

        # Enviar notificação em tempo real via Socket.IO
        # A notificação é adicionada a uma fila thread-safe que é processada
        # por um worker eventlet em background, garantindo entrega em tempo real
        try:
            from app.services.notification_queue_service import add_notification
            notification_data = notification.to_dict()
            add_notification(notification_data)
        except Exception:
            # Falha silenciosa - notificação já está salva no banco
            pass

        # Enviar notificação via WhatsApp se o usuário tiver telefone
        try:
            from app.models.user import User
            from app.utils.whatsapp_helper import send_whatsapp_message, format_phone_number

            user = db.query(User).filter_by(id=user_id).first()

            if user and user.phone:
                phone = format_phone_number(user.phone)
                if phone:
                    whatsapp_message = f"*{title}*\n\n{message}"
                    send_whatsapp_message(phone, whatsapp_message)
        except Exception as e:
            # Falha silenciosa - notificação já está no banco e via Socket.IO
            logging.error("Erro ao enviar notificação WhatsApp")

        return notification

    except Exception as e:
        db.rollback()
        raise e


def notify_travel_approved(user_id, travel_id, destination):
    """Notifica usuário sobre viagem aprovada"""
    return send_notification(
        user_id=user_id,
        title="Viagem Aprovada",
        message=f"Sua viagem para {destination} foi aprovada",
        notification_type=NotificationType.TRAVEL,
        action_url=f"/admin/travels/{travel_id}/edit",
        action_text="Ver Viagem"
    )


def notify_travel_cancelled(user_id, travel_id, destination):
    """Notifica usuário sobre viagem cancelada"""
    return send_notification(
        user_id=user_id,
        title="Viagem Cancelada",
        message=f"Sua viagem para {destination} foi cancelada",
        notification_type=NotificationType.WARNING,
        action_url=f"/admin/travels/{travel_id}/edit",
        action_text="Ver Detalhes"
    )


def notify_ticket_updated(user_id, ticket_id, ticket_subject):
    """Notifica usuário sobre ticket atualizado"""
    return send_notification(
        user_id=user_id,
        title="Ticket Atualizado",
        message=f"O ticket '{ticket_subject}' foi atualizado",
        notification_type=NotificationType.TICKET,
        action_url=f"/admin/tickets/{ticket_id}",
        action_text="Ver Ticket"
    )


def notify_system_message(user_id, title, message):
    """Notifica usuário com mensagem do sistema"""
    return send_notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=NotificationType.SYSTEM
    )
