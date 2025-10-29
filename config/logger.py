# -*- coding: utf-8 -*-
"""
Configuração do sistema de logging da aplicação
"""
import os
import logging
from config.paths import ROOT_DIR

# Define APP_DEBUG com base no valor carregado via .env (através do config/__init__.py)
APP_DEBUG = os.getenv('APP_DEBUG', 'false').lower() == 'true'

# Define o nível de log: DEBUG se estiver em modo de desenvolvimento, ERROR caso contrário
LOG_LEVEL = logging.DEBUG if APP_DEBUG else logging.ERROR

# Define o diretório de logs
LOGS_DIR = os.path.join(ROOT_DIR, 'logs')


def configure_logging():
    """
    Configura o sistema de logging
    """
    os.makedirs(LOGS_DIR, exist_ok=True)  # Garante que a pasta de logs exista

    # Caminhos completos dos arquivos de log
    app_log_path = os.path.join(LOGS_DIR, 'app.log')
    error_log_path = os.path.join(LOGS_DIR, 'error.log')

    # Configuração básica dos logs gerais
    logging.basicConfig(
        filename=app_log_path,
        level=LOG_LEVEL,
        format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler adicional para registrar apenas mensagens de erro em arquivo separado
    error_handler = logging.FileHandler(error_log_path)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
        '%Y-%m-%d %H:%M:%S'
    ))

    # Adiciona o handler de erro ao logger principal
    logging.getLogger().addHandler(error_handler)

    return logging.getLogger()
