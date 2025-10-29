import sys
import argparse
import json
import logging
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

# Inicializar SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False)

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
    parser.add_argument('--host', default='0.0.0.0', help='Host do servidor (padrão: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='Porta do servidor (padrão: 5000)')
    parser.add_argument('--debug', action='store_true', help='Ativa o modo debug')

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

        # Mostrar mensagem apenas no processo principal (evitar duplicação no reloader)
        import os
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            print(f"\n[OK] Servidor iniciado em http://{args.host}:{args.port}")
            print(f"  Modo debug: {'Ativado' if args.debug or DEBUG else 'Desativado'}\n")
            logger.info(f"Servidor Flask iniciado em {args.host}:{args.port} (Debug: {args.debug or DEBUG})")

        debug_mode = args.debug or DEBUG

        # Desabilitar log do eventlet/wsgi
        import os
        os.environ['EVENTLET_NO_GREENDNS'] = 'yes'

        socketio.run(app, debug=debug_mode, host=args.host, port=args.port, log_output=False)
    except Exception as e:
        logger.error(f"Erro ao iniciar o servidor: {str(e)}", exc_info=True)
        print(f"\n[ERRO] Erro ao iniciar o servidor:")
        print(f"  {str(e)}")
        print(f"\n  Dica: Execute 'python main.py --migrate' antes de iniciar o servidor.\n")
        sys.exit(1)