# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, jsonify, session
from app.models.notification import Notification, NotificationType
from app.models.database import get_db
from datetime import datetime
from sqlalchemy import desc


def notifications_list():
    """Lista todas as notificações do usuário"""
    db = get_db()
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('auth.login'))

    # Buscar todas as notificações do usuário ordenadas por data
    notifications = db.query(Notification).filter_by(
        user_id=user_id
    ).order_by(desc(Notification.created_at)).all()

    # Contar notificações não lidas
    unread_count = db.query(Notification).filter_by(
        user_id=user_id,
        is_read=False
    ).count()

    return render_template(
        'pages/notifications/list.html',
        notifications=notifications,
        unread_count=unread_count
    )


def notifications_api_list():
    """API para listar notificações (usado pelo AJAX)"""
    db = get_db()
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'Não autenticado'}), 401

    try:
        # Limite de notificações para o dropdown (últimas 10)
        limit = request.args.get('limit', 10, type=int)

        notifications = db.query(Notification).filter_by(
            user_id=user_id
        ).order_by(desc(Notification.created_at)).limit(limit).all()

        # Contar não lidas
        unread_count = db.query(Notification).filter_by(
            user_id=user_id,
            is_read=False
        ).count()

        return jsonify({
            'notifications': [n.to_dict() for n in notifications],
            'unread_count': unread_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def mark_as_read(notification_id):
    """Marca uma notificação como lida"""
    db = get_db()
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'Não autenticado'}), 401

    try:
        notification = db.query(Notification).filter_by(
            id=notification_id,
            user_id=user_id
        ).first()

        if not notification:
            return jsonify({'error': 'Notificação não encontrada'}), 404

        notification.is_read = True
        notification.read_at = datetime.now()
        db.commit()

        # Contar não lidas restantes
        unread_count = db.query(Notification).filter_by(
            user_id=user_id,
            is_read=False
        ).count()

        return jsonify({
            'success': True,
            'unread_count': unread_count
        })
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


def mark_all_as_read():
    """Marca todas as notificações do usuário como lidas"""
    db = get_db()
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'Não autenticado'}), 401

    try:
        # Atualizar todas as notificações não lidas
        db.query(Notification).filter_by(
            user_id=user_id,
            is_read=False
        ).update({
            'is_read': True,
            'read_at': datetime.now()
        })
        db.commit()

        return jsonify({
            'success': True,
            'message': 'Todas as notificações foram marcadas como lidas',
            'unread_count': 0
        })
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


def delete_notification(notification_id):
    """Deleta uma notificação"""
    db = get_db()
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'Não autenticado'}), 401

    try:
        notification = db.query(Notification).filter_by(
            id=notification_id,
            user_id=user_id
        ).first()

        if not notification:
            return jsonify({'error': 'Notificação não encontrada'}), 404

        db.delete(notification)
        db.commit()

        # Contar não lidas restantes
        unread_count = db.query(Notification).filter_by(
            user_id=user_id,
            is_read=False
        ).count()

        return jsonify({
            'success': True,
            'message': 'Notificação excluída com sucesso',
            'unread_count': unread_count
        })
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


def get_unread_count():
    """Retorna a contagem de notificações não lidas (API)"""
    db = get_db()
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'Não autenticado'}), 401

    try:
        unread_count = db.query(Notification).filter_by(
            user_id=user_id,
            is_read=False
        ).count()

        return jsonify({'unread_count': unread_count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def create_notification(user_id, title, message, notification_type=NotificationType.INFO,
                       action_url=None, action_text=None):
    """
    Função auxiliar para criar notificações
    Pode ser chamada de outros controllers
    """
    db = get_db()

    try:
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            action_url=action_url,
            action_text=action_text
        )

        db.add(notification)
        db.commit()
        db.refresh(notification)

        return notification
    except Exception as e:
        db.rollback()
        raise e
