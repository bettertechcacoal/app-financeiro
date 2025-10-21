# config/app.py

import os

# Flask
SECRET_KEY = os.getenv('SECRET_KEY', 'sua-chave-secreta-aqui-mude-em-producao')
DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
