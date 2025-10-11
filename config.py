# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configurações da aplicação"""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'sua-chave-secreta-aqui-mude-em-producao')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    # Auth Service
    AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://localhost:8000')
    AUTH_SERVICE_TIMEOUT = int(os.getenv('AUTH_SERVICE_TIMEOUT', '10'))

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')


config = Config()
