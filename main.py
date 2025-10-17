import sys
import argparse
import json
from flask import Flask
from flask_socketio import SocketIO
from routes import register_routes
from config import config
from app.models.database import init_db

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['DEBUG'] = config.DEBUG

# Inicializar SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

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

def make_migration(message):
    """Cria uma nova migration"""
    from alembic.config import Config
    from alembic import command

    print(f"[MIGRATION] Criando migration: {message}")

    alembic_cfg = Config("alembic.ini")

    try:
        command.revision(alembic_cfg, message=message, autogenerate=False)
        print("[SUCCESS] Migration criada com sucesso!")
        return True
    except Exception as e:
        print(f"[ERROR] Erro ao criar migration: {str(e)}")
        return False

def run_migrations():
    """Executa as migrations pendentes"""
    from alembic.config import Config
    from alembic import command

    print("[MIGRATION] Executando migrations do banco de dados...")

    alembic_cfg = Config("alembic.ini")

    try:
        command.upgrade(alembic_cfg, "head")
        print("[SUCCESS] Migrations executadas com sucesso!")
        return True
    except Exception as e:
        print(f"[ERROR] Erro ao executar migrations: {str(e)}")
        return False

def migrate_fresh():
    """Drop todas as tabelas e recria (migrate:fresh)"""
    from alembic.config import Config
    from alembic import command

    print("[MIGRATION] Executando migrate:fresh...")
    print("[WARNING] Isso vai APAGAR todos os dados do banco!")

    alembic_cfg = Config("alembic.ini")

    try:
        # Downgrade para base (remove tudo)
        print("[STEP 1/2] Fazendo downgrade de todas as migrations...")
        command.downgrade(alembic_cfg, "base")

        # Upgrade para head (recria tudo)
        print("[STEP 2/2] Executando todas as migrations...")
        command.upgrade(alembic_cfg, "head")

        print("[SUCCESS] Migrate:fresh executado com sucesso!")
        return True
    except Exception as e:
        print(f"[ERROR] Erro ao executar migrate:fresh: {str(e)}")
        return False

def migrate_rollback():
    """Faz rollback da última migration"""
    from alembic.config import Config
    from alembic import command

    print("[MIGRATION] Fazendo rollback da última migration...")

    alembic_cfg = Config("alembic.ini")

    try:
        command.downgrade(alembic_cfg, "-1")
        print("[SUCCESS] Rollback executado com sucesso!")
        return True
    except Exception as e:
        print(f"[ERROR] Erro ao executar rollback: {str(e)}")
        return False

if __name__ == '__main__':
    # Configurar argumentos de linha de comando
    parser = argparse.ArgumentParser(description='Servidor Flask do App Financeiro')

    # Comandos de migrations (estilo Laravel)
    parser.add_argument('--make-migration', type=str, metavar='MESSAGE', help='Cria uma nova migration (ex: create_users_table)')
    parser.add_argument('--migrate', action='store_true', help='Executa as migrations pendentes')
    parser.add_argument('--migrate-fresh', action='store_true', help='Drop todas as tabelas e recria (APAGA TODOS OS DADOS)')
    parser.add_argument('--migrate-rollback', action='store_true', help='Faz rollback da última migration')

    # Opções do servidor
    parser.add_argument('--host', default='0.0.0.0', help='Host para o servidor (padrão: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='Porta para o servidor (padrão: 5000)')
    parser.add_argument('--debug', action='store_true', help='Ativa o modo debug')

    args = parser.parse_args()

    # Processar comandos de migration
    if args.make_migration:
        success = make_migration(args.make_migration)
        sys.exit(0 if success else 1)

    if args.migrate:
        success = run_migrations()
        sys.exit(0 if success else 1)

    if args.migrate_fresh:
        success = migrate_fresh()
        sys.exit(0 if success else 1)

    if args.migrate_rollback:
        success = migrate_rollback()
        sys.exit(0 if success else 1)

    # Caso contrário, iniciar o servidor com SocketIO
    # Inicializar banco de dados apenas quando o servidor for iniciado
    with app.app_context():
        init_db()

        # Inicializar scheduler de tarefas automáticas
        from app.services.scheduler_service import init_scheduler
        init_scheduler(app)
        print("[SCHEDULER] Sistema de sincronização automática inicializado")

    debug_mode = args.debug or config.DEBUG
    socketio.run(app, debug=debug_mode, host=args.host, port=args.port)