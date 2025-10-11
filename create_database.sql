-- Script para criar o banco de dados do App Financeiro
-- Execute este script como superusuário do PostgreSQL

-- Criar banco de dados
CREATE DATABASE app_financeiro
    WITH
    OWNER = demo
    ENCODING = 'UTF8'
    LC_COLLATE = 'Portuguese_Brazil.1252'
    LC_CTYPE = 'Portuguese_Brazil.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

COMMENT ON DATABASE app_financeiro
    IS 'Banco de dados do App Financeiro';

-- As tabelas serão criadas automaticamente pelo SQLAlchemy ao iniciar o servidor
