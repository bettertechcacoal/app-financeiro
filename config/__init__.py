# config/__init__.py

import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Importações centralizadas
from .app import SECRET_KEY, DEBUG
from .auth import AUTH_SERVICE_URL, AUTH_SERVICE_TIMEOUT, JWT_SECRET_KEY, JWT_ALGORITHM
from .paths import ROOT_DIR
