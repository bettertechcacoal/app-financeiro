# config/app.py

import os

# Flask
SECRET_KEY = os.getenv('SECRET_KEY', 'sua-chave-secreta-aqui-mude-em-producao')
DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

# Evolution API (WhatsApp)
EVOLUTION_API_URL = os.getenv('EVOLUTION_API_URL', 'http://localhost:8080')
EVOLUTION_API_KEY = os.getenv('EVOLUTION_API_KEY', 'change-me-to-secure-key')
