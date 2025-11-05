import eventlet
eventlet.monkey_patch()

import sys
import argparse
import json
import logging
import os
from flask import Flask
from flask_socketio import SocketIO
from routes import register_routes
from config import SECRET_KEY, DEBUG
from config.logger import configure_logging
from app.models.database import init_db

# Configurar sistema de logging
logger = configure_logging()

# Desabilitar logs do Werkzeug
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = DEBUG
app.config['APP_NAME'] = os.getenv('APP_NAME', 'Financeiro')

# Inicializar SocketIO
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='eventlet',
    logger=False,
    engineio_logger=False
)

# Adicionar filtros Jinja customizados
@app.template_filter('from_json')
def from_json_filter(value):
    """Converte string JSON para objeto Python"""
    if not value:
        return []
    try:
        return json.loads(value)
    except:
        return []

register_routes(app)

# Registrar error handlers personalizados
from app.error_handlers import register_error_handlers
register_error_handlers(app)

# Registrar eventos Socket.IO
from app.socketio_events import register_socketio_events
register_socketio_events(socketio)

# Fechar sessões do banco automaticamente após cada requisição
from app.models.database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    """Remove a sessão do banco de dados ao final de cada requisição"""
    try:
        if exception:
            db_session.rollback()
        else:
            db_session.commit()
    except:
        db_session.rollback()
    finally:
        db_session.remove()

def run_migrations():
    """Executa as migrations pendentes"""
    from alembic.config import Config
    from alembic import command

    alembic_cfg = Config("alembic.ini")

    try:
        command.upgrade(alembic_cfg, "head")
        print("\n[OK] Migrations executadas com sucesso!\n")
        return True
    except Exception as e:
        print(f"\n[ERRO] Erro ao executar migrations:")
        print(f"  {str(e)}\n")
        return False

def migrate_fresh():
    """Drop todas as tabelas e recria (migrate:fresh)"""
    from alembic.config import Config
    from alembic import command

    alembic_cfg = Config("alembic.ini")

    try:
        command.downgrade(alembic_cfg, "base")
        command.upgrade(alembic_cfg, "head")
        return True
    except Exception as e:
        print(f"\nErro ao recriar banco de dados: {str(e)}\n")
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Servidor Flask do App Financeiro')

    # Comandos de migrations
    parser.add_argument('--migrate', action='store_true', help='Executa as migrations pendentes')
    parser.add_argument('--migrate-fresh', action='store_true', help='Recria o banco de dados do zero')

    # Opções do servidor
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=int(os.getenv('APP_PORT', 5000)))
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()

    # Processar comandos de migration
    if args.migrate:
        success = run_migrations()
        sys.exit(0 if success else 1)

    if args.migrate_fresh:
        success = migrate_fresh()
        sys.exit(0 if success else 1)

    # Iniciar o servidor
    try:
        logger.info("Iniciando aplicação...")

        with app.app_context():
            logger.info("Banco de dados inicializado")

            # Inicializar scheduler de tarefas automáticas
            from app.services.scheduler_service import init_scheduler
            init_scheduler(app)
            logger.info("Scheduler de tarefas inicializado")

        # Worker que processa fila de notificações em tempo real
        # Utiliza eventlet para não bloquear o servidor
        def notification_worker():
            import eventlet
            from app.services.notification_queue_service import get_queue

            notification_queue = get_queue()

            while True:
                try:
                    # Verificar fila a cada 100ms
                    eventlet.sleep(0.1)

                    # Processar todas as notificações pendentes
                    while not notification_queue.empty():
                        notif_data = notification_queue.get_nowait()
                        user_id = notif_data.get('user_id')

                        if user_id:
                            # Emitir notificação para a room específica do usuário
                            # Rooms são gerenciadas automaticamente pelo Flask-SocketIO
                            socketio.emit(
                                'new_notification',
                                notif_data,
                                room=f'user_{user_id}',
                                namespace='/'
                            )
                except:
                    continue

        # Iniciar worker em background
        socketio.start_background_task(notification_worker)

        # Mostrar mensagem apenas no processo principal (evitar duplicação no reloader)
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            print(f"\n[OK] Servidor iniciado em http://{args.host}:{args.port}")
            print(f"  Modo debug: {'Ativado' if args.debug or DEBUG else 'Desativado'}\n")
            logger.info(f"Servidor Flask iniciado em {args.host}:{args.port} (Debug: {args.debug or DEBUG})")

        debug_mode = args.debug or DEBUG

        # Desabilitar log do eventlet/wsgi
        os.environ['EVENTLET_NO_GREENDNS'] = 'yes'

        socketio.run(app, debug=debug_mode, host=args.host, port=args.port, log_output=False)
    except Exception as e:
        logger.error(f"Erro ao iniciar o servidor: {str(e)}", exc_info=True)
        print(f"\n[ERRO] Erro ao iniciar o servidor:")
        print(f"  {str(e)}")
        print(f"\n  Dica: Execute 'python main.py --migrate' antes de iniciar o servidor.\n")
        sys.exit(1)