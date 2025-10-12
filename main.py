import sys
import argparse
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

# Inicializar banco de dados
with app.app_context():
    init_db()

register_routes(app)

# Registrar eventos Socket.IO
from app.socketio_events import register_socketio_events
register_socketio_events(socketio)

def run_migrations():
    """Executa as migrations do Alembic"""
    from alembic.config import Config
    from alembic import command
    import os

    print("[MIGRATION] Executando migrations do banco de dados...")

    # Configurar Alembic
    alembic_cfg = Config("alembic.ini")

    try:
        # Executar upgrade para a última versão
        command.upgrade(alembic_cfg, "head")
        print("[SUCCESS] Migrations executadas com sucesso!")
        return True
    except Exception as e:
        print(f"[ERROR] Erro ao executar migrations: {str(e)}")
        return False

if __name__ == '__main__':
    # Configurar argumentos de linha de comando
    parser = argparse.ArgumentParser(description='Servidor Flask do App Financeiro')
    parser.add_argument('--migration', action='store_true', help='Executa as migrations do banco de dados')
    parser.add_argument('--host', default='0.0.0.0', help='Host para o servidor (padrão: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='Porta para o servidor (padrão: 5000)')
    parser.add_argument('--debug', action='store_true', help='Ativa o modo debug')

    args = parser.parse_args()

    # Se o argumento --migration foi passado, executar migrations
    if args.migration:
        success = run_migrations()
        sys.exit(0 if success else 1)

    # Caso contrário, iniciar o servidor com SocketIO
    debug_mode = args.debug or config.DEBUG
    socketio.run(app, debug=debug_mode, host=args.host, port=args.port)