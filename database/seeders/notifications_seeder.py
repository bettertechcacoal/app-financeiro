# -*- coding: utf-8 -*-
"""
Seeder de Notificações
Popula a tabela de notificações com dados de teste
"""
import sys
from config import ROOT_DIR

sys.path.insert(0, ROOT_DIR)

from app.models.user import User
from app.models.notification import Notification, NotificationType
from app.models.database import SessionLocal
from datetime import datetime, timedelta
from sqlalchemy import text


def seed_notifications():
    """Cria notificações de teste para demonstração do sistema"""
    db = SessionLocal()

    try:
        # Buscar usuário para vincular notificações (usar primeiro usuário encontrado)
        user = db.query(User).first()

        if not user:
            print("[ERRO] Nenhum usuário encontrado. Execute o users_seeder primeiro")
            return

        # Limpar notificações existentes do usuário
        db.query(Notification).filter_by(user_id=user.id).delete()

    now = datetime.now()

    # Criar notificações de diferentes tipos
    notifications_data = [
        {
            'user_id': user.id,
            'title': 'Bem-vindo ao Sistema!',
            'message': 'Seja bem-vindo ao sistema de gestão financeira. Explore as funcionalidades e comece a gerenciar seus dados.',
            'type': NotificationType.SUCCESS,
            'action_url': '/admin/dashboard',
            'action_text': 'Ir para Dashboard',
            'is_read': False,
            'created_at': now - timedelta(minutes=5)
        },
        {
            'user_id': user.id,
            'title': 'Nova viagem aprovada',
            'message': 'Sua viagem para Porto Velho foi aprovada. Você já pode providenciar a reserva do veículo.',
            'type': NotificationType.TRAVEL,
            'action_url': '/admin/travels',
            'action_text': 'Ver Viagens',
            'is_read': False,
            'created_at': now - timedelta(hours=1)
        },
        {
            'user_id': user.id,
            'title': 'Atenção: Prazo próximo',
            'message': 'O prazo para conclusão da viagem a Ariquemes está chegando. Verifique os pendências.',
            'type': NotificationType.WARNING,
            'action_url': '/admin/travels',
            'action_text': 'Ver Detalhes',
            'is_read': True,
            'read_at': now - timedelta(hours=3),
            'created_at': now - timedelta(hours=4)
        },
        {
            'user_id': user.id,
            'title': 'Erro ao sincronizar dados',
            'message': 'Houve um erro ao sincronizar os dados com o Movidesk. Tente novamente mais tarde.',
            'type': NotificationType.ERROR,
            'action_url': '/admin/integrations',
            'action_text': 'Ver Integrações',
            'is_read': True,
            'read_at': now - timedelta(hours=5),
            'created_at': now - timedelta(hours=6)
        },
        {
            'user_id': user.id,
            'title': 'Atualização do sistema',
            'message': 'O sistema será atualizado amanhã às 22h. Pode haver indisponibilidade por alguns minutos.',
            'type': NotificationType.INFO,
            'action_url': None,
            'action_text': None,
            'is_read': False,
            'created_at': now - timedelta(days=1)
        },
        {
            'user_id': user.id,
            'title': 'Manutenção programada',
            'message': 'Manutenção programada do sistema será realizada no próximo sábado das 00h às 06h.',
            'type': NotificationType.SYSTEM,
            'action_url': None,
            'action_text': None,
            'is_read': True,
            'read_at': now - timedelta(days=2),
            'created_at': now - timedelta(days=3)
        },
        {
            'user_id': user.id,
            'title': 'Viagem cancelada',
            'message': 'A viagem para Vilhena foi cancelada. Verifique os motivos do cancelamento.',
            'type': NotificationType.WARNING,
            'action_url': '/admin/travels',
            'action_text': 'Ver Viagens',
            'is_read': True,
            'read_at': now - timedelta(days=4),
            'created_at': now - timedelta(days=5)
        },
        {
            'user_id': user.id,
            'title': 'Viagem em andamento',
            'message': 'Sua viagem para Ji-Paraná está em andamento. Boa viagem!',
            'type': NotificationType.TRAVEL,
            'action_url': '/admin/travels',
            'action_text': 'Ver Viagens',
            'is_read': True,
            'read_at': now - timedelta(days=6),
            'created_at': now - timedelta(days=7)
        }
    ]

        # Inserir notificações
        for notif_data in notifications_data:
            notification = Notification(**notif_data)
            db.add(notification)

        # Ajustar sequência de auto incremento do PostgreSQL
        db.execute(text("SELECT setval(pg_get_serial_sequence('notifications', 'id'), (SELECT COALESCE(MAX(id), 1) FROM notifications))"))
        db.commit()

        print("[SUCCESS] Seeder de notificações executado com sucesso")

    except Exception as e:
        db.rollback()
        print(f"[ERRO] {type(e).__name__}: {str(e).split(chr(10))[0]}")
    finally:
        db.close()


if __name__ == '__main__':
    seed_notifications()
