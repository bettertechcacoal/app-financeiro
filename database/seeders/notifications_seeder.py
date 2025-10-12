# -*- coding: utf-8 -*-
from app.models.user import User
from app.models.notification import Notification, NotificationType
from app.models.database import get_db
from datetime import datetime, timedelta


def seed_notifications():
    """Criar notificações de teste"""
    db = get_db()

    print("\n[SEEDER] Criando notificações de teste...")

    # Buscar o usuário demo
    user = db.query(User).filter_by(email='demo@demo.com').first()

    if not user:
        print("[ERROR] Usuário demo@demo.com não encontrado. Execute o users_seeder primeiro.")
        return

    # Limpar notificações existentes do usuário demo (para evitar duplicatas)
    db.query(Notification).filter_by(user_id=user.id).delete()
    db.commit()

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

    db.commit()

    total = len(notifications_data)
    unread = sum(1 for n in notifications_data if not n['is_read'])

    print(f"[SUCCESS] {total} notificações criadas com sucesso!")
    print(f"          - {unread} não lidas")
    print(f"          - {total - unread} lidas")
    print(f"          (Removidas notificações de tickets e cadastro de clientes)")


if __name__ == '__main__':
    seed_notifications()
