# config/paths.py

import os

# Pega o diretório do arquivo atual (config/paths.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Sobe um nível para chegar na raiz (app-financeiro/)
ROOT_DIR = os.path.dirname(current_dir)
