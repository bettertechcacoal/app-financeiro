# 📦 Guia de Migrations com Alembic

Este projeto agora usa **Alembic** para gerenciar as migrations do banco de dados.

## 🚀 Comandos Disponíveis

### Executar Migrations
```bash
# Opção 1: Via server.py
python server.py --migration

# Opção 2: Via Alembic diretamente
alembic upgrade head
```

### Criar Nova Migration
```bash
# Migration automática (detecta mudanças nos modelos)
alembic revision --autogenerate -m "descrição da alteração"

# Migration manual
alembic revision -m "descrição da alteração"
```

### Ver Status das Migrations
```bash
# Ver histórico de migrations
alembic history

# Ver versão atual do banco
alembic current

# Ver migrations pendentes
alembic show
```

### Reverter Migrations
```bash
# Voltar uma migration
alembic downgrade -1

# Voltar para versão específica
alembic downgrade <revision_id>

# Voltar todas
alembic downgrade base
```

## 📁 Estrutura de Arquivos

```
app-financeiro/
├── database/
│   └── migrations/              # Diretório principal do Alembic
│       ├── versions/            # Arquivos de migration
│       │   └── 001_initial_schema.py
│       ├── env.py               # Configuração do ambiente (carrega .env)
│       └── script.py.mako       # Template para novas migrations
├── alembic.ini                  # Configuração do Alembic (não precisa editar)
├── .env                         # Variáveis de ambiente (DB_USER, DB_PASSWORD, etc)
└── server.py                    # Servidor com suporte a --migration
```

## ⚙️ Como Funciona

### Carregamento de Configurações

O sistema de migrations está configurado para usar automaticamente as variáveis do arquivo `.env`:

1. **env.py** (database/migrations/env.py:12-27)
   - Carrega o arquivo `.env` usando `python-dotenv`
   - Lê as variáveis `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`
   - Constrói a URL de conexão dinamicamente
   - Injeta a URL no contexto do Alembic

2. **alembic.ini**
   - Não contém credenciais hardcoded
   - Apenas configurações gerais do Alembic
   - A URL do banco é configurada via `env.py`

3. **server.py**
   - Comando `python server.py --migration` executa `alembic upgrade head`
   - Usa as mesmas configurações do `.env`

## 🔧 Configuração Inicial

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente
Certifique-se que o arquivo `.env` contém:
```env
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=app_financeiro
```

**Importante:** O Alembic carrega automaticamente as configurações do arquivo `.env`. Não é necessário editar o `alembic.ini`.

### 3. Criar o Banco de Dados
```bash
# Conectar ao PostgreSQL
psql -U postgres

# Criar banco
CREATE DATABASE app_financeiro;

# Sair
\q
```

### 4. Executar Primeira Migration
```bash
# Opção 1: Via comando personalizado (recomendado)
python server.py --migration

# Opção 2: Via Alembic diretamente
alembic upgrade head
```

**Nota:**
- Se o banco já possui tabelas, use `alembic stamp head` para marcar como atualizado sem executar migrations
- Todas as configurações de banco são lidas do arquivo `.env` automaticamente

## 📝 Exemplo: Criar Nova Migration

### 1. Modificar o Modelo
```python
# app/models/client.py
class Client(Base):
    __tablename__ = 'clients'

    # ... campos existentes ...

    # Novo campo
    cpf = Column(String(14), nullable=True)
```

### 2. Gerar Migration Automática
```bash
alembic revision --autogenerate -m "add cpf field to clients"
```

### 3. Revisar o Arquivo Gerado
```python
# alembic/versions/xxx_add_cpf_field_to_clients.py
def upgrade() -> None:
    op.add_column('clients', sa.Column('cpf', sa.String(length=14), nullable=True))

def downgrade() -> None:
    op.drop_column('clients', 'cpf')
```

### 4. Aplicar Migration
```bash
python server.py --migration
```

## ✅ Migration Atual

**Versão 001:** `initial_schema`
- Cria todas as tabelas do banco de dados:
  - `organizations` - Organizações do Movidesk
  - `clients` - Clientes do sistema
  - `client_organizations` - Relacionamento muitos-para-muitos entre clientes e organizações
  - `sync_logs` - Logs de sincronização
  - `tickets` - Tickets do Movidesk
- Adiciona índices para melhor performance
- Adiciona constraints e chaves estrangeiras

## 🎯 Boas Práticas

1. **Sempre revisar migrations geradas automaticamente**
   - O Alembic pode não detectar todas as mudanças
   - Verifique se o `upgrade()` e `downgrade()` estão corretos

2. **Testar migrations antes de aplicar em produção**
   ```bash
   # Aplicar
   alembic upgrade head

   # Testar rollback
   alembic downgrade -1

   # Reaplicar
   alembic upgrade head
   ```

3. **Manter migrations pequenas e focadas**
   - Uma migration por funcionalidade
   - Facilita rollback e debug

4. **Nunca editar migrations já aplicadas**
   - Se precisar corrigir, crie uma nova migration

## 🐛 Troubleshooting

### Erro: "Can't locate revision identified by 'xxx'"
```bash
# Resetar o histórico
alembic stamp head
```

### Erro: "Target database is not up to date"
```bash
# Verificar versão atual
alembic current

# Atualizar para a última versão
alembic upgrade head
```

### Erro de Conexão com Banco

**Verificar variáveis de ambiente:**
```bash
# Windows (CMD)
echo %DB_USER%
echo %DB_PASSWORD%
echo %DB_HOST%
echo %DB_NAME%

# Windows (PowerShell)
$env:DB_USER
$env:DB_PASSWORD

# Linux/Mac
env | grep DB_
```

**Testar conexão:**
```bash
psql -U postgres -d app_financeiro
```

### Verificar se o .env está sendo carregado

O arquivo `database/migrations/env.py` já está configurado para carregar automaticamente:
```python
# Carregar variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

# Configurar a URL do banco de dados
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
# ... etc
```

**Se ainda houver problemas, verifique:**
1. Se o arquivo `.env` existe na raiz do projeto
2. Se a dependência `python-dotenv` está instalada (`pip install python-dotenv`)
3. Se as variáveis estão no formato correto:
   - ✅ `DB_USER=postgres`
   - ❌ `DB_USER = postgres` (sem espaços)
   - ❌ `DB_USER="postgres"` (sem aspas desnecessárias)

## 📚 Referências

- [Documentação Oficial do Alembic](https://alembic.sqlalchemy.org/)
- [Tutorial de Migrations](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
