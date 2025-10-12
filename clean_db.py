# -*- coding: utf-8 -*-
"""
Script para limpar completamente o banco de dados
"""
import os
from sqlalchemy import create_engine, text

def clean_database():
    """Limpa completamente o banco de dados"""

    # Configuração do banco de dados
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'eloconta')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'app_financeiro')

    DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Criar engine
    engine = create_engine(DATABASE_URI)

    print("\n" + "="*60)
    print("LIMPANDO BANCO DE DADOS COMPLETAMENTE")
    print("="*60 + "\n")

    with engine.connect() as conn:
        # Encerrar todas as conexões ativas
        print("[1/3] Encerrando conexões ativas...")
        conn.execute(text("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = 'app_financeiro'
            AND pid <> pg_backend_pid()
        """))
        conn.commit()

        # Dropar o schema public
        print("[2/3] Removendo schema public...")
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.commit()

        # Recriar o schema public
        print("[3/3] Recriando schema public...")
        conn.execute(text("CREATE SCHEMA public"))
        conn.execute(text("GRANT ALL ON SCHEMA public TO postgres"))
        conn.execute(text("GRANT ALL ON SCHEMA public TO public"))
        conn.commit()

    print("\n" + "="*60)
    print("BANCO DE DADOS LIMPO COM SUCESSO!")
    print("="*60 + "\n")

if __name__ == '__main__':
    clean_database()
