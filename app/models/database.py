# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Base para os modelos
Base = declarative_base()

# Configuração do banco de dados
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'app_financeiro')

# String de conexão
DATABASE_URL = f"postgresql://{quote_plus(DB_USER)}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Engine do SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Scoped session para thread-safety
db_session = scoped_session(SessionLocal)


def init_db():
    """Inicializa o banco de dados criando todas as tabelas"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Retorna uma sessão do banco de dados"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
