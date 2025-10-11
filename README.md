# App Financeiro - Sistema Completo

Sistema de gestão financeira com integração ao Movidesk para sincronização de organizações, gerenciamento de clientes e visualização de tickets.

## Funcionalidades Implementadas

### 1. Sistema de Autenticação
- Integração com Auth-Service (microserviço de autenticação)
- Login com JWT tokens
- Proteção de rotas com middleware de autenticação
- Gerenciamento de sessões

### 2. Sistema de Integração com Movidesk
- Card "Integrações" no dashboard principal
- Tela de seleção de integrações disponíveis
- Tela de opções do Movidesk (Tickets e Organizações)
- Sistema de sincronização de organizações
- Sincronização de tickets do Movidesk
- Vinculação de clientes a organizações do Movidesk

### 3. Gerenciamento de Clientes
- Card "Clientes" no dashboard
- Lista de clientes cadastrados com busca
- Cadastro e edição de clientes com tabs organizadas
- Vinculação múltipla de clientes a organizações do Movidesk
- Validação de campos obrigatórios
- Configuração de ciclos de cobrança (fixo ou mensal)
- Cache de tabs usando localStorage
- Persistência de dados ao salvar (permanece na mesma página)

### 4. Gerenciamento de Tickets
- Visualização de tickets por cliente
- Lista de tickets por organização vinculada
- Integração com API do Movidesk
- Filtros e busca de tickets
- Sincronização automática de tickets

### 5. Sistema de Viagens
- Cadastro de viagens
- Gerenciamento de solicitações de viagem
- Aprovação de viagens
- Controle de estados e cidades

### 6. Perfil do Usuário
- Visualização de dados do usuário
- Edição de perfil
- Gerenciamento de grupos e permissões

### 7. Sistema de Breadcrumbs
- Navegação hierárquica em todas as telas
- Componente reutilizável para breadcrumbs
- Integrado em todas as páginas do sistema

### 8. Banco de Dados
- PostgreSQL com SQLAlchemy ORM
- Sistema de migrations com Alembic
- Modelos completos:
  - Organizations (organizações do Movidesk)
  - Clients (clientes do sistema)
  - ClientOrganization (relacionamento many-to-many)
  - Tickets (tickets do Movidesk)
  - Users (usuários do sistema)
  - Groups (grupos de permissões)
  - States e Cities (localização)
  - Travels (viagens)
- Seeders para popular dados iniciais

## Estrutura do Projeto

```
app-financeiro/
├── app/
│   ├── controllers/
│   │   ├── auth/
│   │   │   └── login_controller.py
│   │   ├── clients/
│   │   │   └── clients_controller.py
│   │   ├── dashboard/
│   │   │   └── dashboard_controller.py
│   │   ├── integrations/
│   │   │   └── integrations_controller.py
│   │   ├── tickets/
│   │   │   └── tickets_controller.py
│   │   ├── profile_controller.py
│   │   └── travels_controller.py
│   ├── models/
│   │   ├── database.py
│   │   ├── organization.py
│   │   ├── client.py
│   │   ├── client_organization.py
│   │   ├── ticket.py
│   │   ├── user.py
│   │   ├── group.py
│   │   ├── user_group.py
│   │   ├── state.py
│   │   ├── city.py
│   │   ├── travel.py
│   │   └── sync_log.py
│   └── services/
│       ├── auth_service.py
│       ├── client_service.py
│       ├── movidesk_service.py
│       └── ticket_service.py
├── database/
│   ├── migrations/
│   │   └── versions/
│   │       ├── 001_create_groups_table.py
│   │       ├── 002_create_users_table.py
│   │       ├── 003_create_user_groups_table.py
│   │       ├── 004_create_states_table.py
│   │       ├── 005_create_cities_table.py
│   │       ├── 006_create_travels_table.py
│   │       ├── 007_create_organizations_table.py
│   │       ├── 008_create_clients_table.py
│   │       ├── 009_create_client_organizations_table.py
│   │       ├── 010_create_sync_logs_table.py
│   │       ├── 011_create_tickets_table.py
│   │       └── 012_add_billing_fields_to_clients.py
│   └── seeders/
│       ├── database_seeder.py
│       ├── groups_seeder.py
│       ├── users_seeder.py
│       └── cities_seeder.py
├── templates/
│   ├── components/
│   │   └── breadcrumbs.html
│   ├── pages/
│   │   ├── auth/
│   │   │   └── login.html
│   │   ├── clients/
│   │   │   ├── manage.html
│   │   │   └── form.html
│   │   ├── integrations/
│   │   │   ├── list.html
│   │   │   ├── movidesk_options.html
│   │   │   ├── movidesk_organizations.html
│   │   │   ├── movidesk_tickets.html
│   │   │   └── organization_edit.html
│   │   ├── tickets/
│   │   │   ├── list.html
│   │   │   └── view.html
│   │   ├── travels/
│   │   │   ├── list.html
│   │   │   └── form.html
│   │   ├── profile/
│   │   │   └── profile.html
│   │   └── dashboard.html
│   └── base.html
├── static/
│   └── css/
│       └── dashboard.css
├── test/
│   ├── test_login_flow.py
│   └── test_all_routes.py
├── .env
├── alembic.ini
├── config.py
├── routes.py
├── main.py
├── requirements.txt
└── README.md
```

## Configuração

### 1. Requisitos
- Python 3.8+
- PostgreSQL 12+
- Auth-Service rodando em http://localhost:8000

### 2. Instalação

```bash
# Clonar/acessar o diretório
cd app-financeiro

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configurar Banco de Dados

Criar banco de dados PostgreSQL:

```sql
CREATE DATABASE app_financeiro;
```

### 4. Configurar Variáveis de Ambiente

Editar o arquivo `.env`:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui-mude-em-producao

# Auth Service Configuration
AUTH_SERVICE_URL=http://localhost:8000
AUTH_SERVICE_TIMEOUT=10

# JWT Configuration
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256

# Database Configuration
DB_USER=postgres
DB_PASSWORD=sua-senha-postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=app_financeiro

# Movidesk API Configuration
MOVIDESK_TOKEN=seu-token-movidesk-aqui
```

### 5. Executar Migrations

```bash
# Executar todas as migrations
alembic upgrade head
```

### 6. Popular Dados Iniciais (Opcional)

```bash
# Popular grupos e usuários
python database/seeders/database_seeder.py
```

### 7. Inicializar o Sistema

```bash
python main.py
```

O sistema estará disponível em `http://localhost:5000`

**Credenciais padrão:**
- Email: `demo@demo.com`
- Senha: `demo123`

## Fluxo de Uso

### Sincronizar Organizações do Movidesk

1. Acesse o dashboard
2. Clique no card "Integrações"
3. Clique em "Movidesk"
4. Clique em "Organizações"
5. Clique no botão "Sincronizar Agora"
6. Aguarde a sincronização (as organizações serão importadas do Movidesk)

### Cadastrar um Cliente

1. Acesse o dashboard
2. Clique no card "Clientes"
3. Clique em "Novo Cliente"
4. Preencha os dados nas abas:
   - **Pessoa**: Dados básicos e vinculação com Movidesk
   - **Cobrança**: Configuração do ciclo de cobrança (fixo ou mensal)
   - **Endereços**: Endereço completo
   - **Módulos**: Módulos do sistema (em desenvolvimento)
   - **Contatos**: Pessoas de contato (em desenvolvimento)
5. Clique em "Salvar"

### Visualizar Tickets de um Cliente

1. Acesse o dashboard
2. Clique no card "Tickets"
3. Localize o cliente na lista
4. Clique em "Visualizar"
5. Veja os tickets separados por organização vinculada

## Rotas da API

### Autenticação

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Redireciona para login ou dashboard |
| GET/POST | `/login` | Tela de login |
| GET | `/logout` | Logout do sistema |

### Dashboard

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/admin/dashboard` | Dashboard principal |

### Clientes

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/admin/clients` | Lista clientes |
| GET | `/admin/clients/new` | Formulário novo cliente |
| POST | `/admin/clients/create` | Cria cliente |
| GET | `/admin/clients/<id>/edit` | Formulário edição |
| POST | `/admin/clients/<id>/update` | Atualiza cliente |
| POST | `/admin/clients/<id>/delete` | Remove cliente |
| GET | `/admin/api/organizations` | Lista organizações (API) |
| GET | `/admin/api/clients` | Lista clientes (API) |

### Tickets

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/admin/tickets` | Lista clientes para visualizar tickets |
| GET | `/admin/tickets/client/<id>` | Visualiza tickets do cliente |

### Integrações

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/admin/integrations` | Lista integrações |
| GET | `/admin/integrations/movidesk` | Opções Movidesk |
| GET | `/admin/integrations/movidesk/organizations` | Tela sincronização organizações |
| POST | `/admin/integrations/movidesk/organizations/sync` | Sincroniza organizações |
| GET | `/admin/integrations/movidesk/tickets` | Tela sincronização tickets |
| POST | `/admin/integrations/movidesk/tickets/sync` | Sincroniza tickets |
| GET | `/admin/organizations/<id>/edit` | Editar organização |
| POST | `/admin/organizations/<id>/update` | Atualizar organização |
| GET | `/admin/api/clients/unlinked` | Lista clientes não vinculados |
| POST | `/admin/organizations/<id>/clients/<id>/link` | Vincular cliente |
| POST | `/admin/organizations/<id>/clients/<id>/unlink` | Desvincular cliente |
| POST | `/admin/organizations/<id>/toggle-status` | Ativar/desativar organização |

### Viagens

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/admin/travels` | Lista viagens |
| GET | `/admin/travels/new` | Formulário nova viagem |
| POST | `/admin/travels/create` | Cria viagem |
| GET | `/admin/travels/<id>/edit` | Formulário edição |
| POST | `/admin/travels/<id>/update` | Atualiza viagem |
| GET | `/admin/travels/<id>/delete` | Remove viagem |
| GET | `/admin/travels/<id>/approve` | Aprovar viagem |

### Perfil

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/admin/profile` | Visualizar perfil |
| POST | `/admin/profile/update` | Atualizar perfil |

## Modelos de Dados

### Organization

```python
{
    'id': String(50),              # ID do Movidesk
    'business_name': String(255),  # Razão social
    'person_type': String(20),     # Tipo de pessoa
    'is_active': Boolean,          # Ativo/Inativo
    'created_at': DateTime,
    'updated_at': DateTime
}
```

### Client

```python
{
    'id': Integer,                 # ID autoincrement
    'name': String(255),           # Nome completo
    'email': String(255),          # Email
    'phone': String(50),           # Telefone
    'document': String(50),        # CPF/CNPJ (único)
    'organization_id': String(50), # FK para organizations (legado)
    'address': String(500),        # Endereço
    'city': String(100),           # Cidade
    'state': String(2),            # UF
    'zipcode': String(20),         # CEP
    'billing_cycle': Integer,      # Ciclo de cobrança em dias
    'billing_day': Integer,        # Dia do mês para cobrança
    'billing_cycle_type': String(20),  # Tipo: 'fixo' ou 'mensal'
    'fixed_start_day': Integer,    # Dia de início (ciclo fixo)
    'created_at': DateTime,
    'updated_at': DateTime
}
```

### ClientOrganization (Tabela de Relacionamento)

```python
{
    'id': Integer,                 # ID autoincrement
    'client_id': Integer,          # FK para clients
    'organization_id': String(50), # FK para organizations
    'created_at': DateTime
}
```

### Ticket

```python
{
    'id': Integer,                 # ID do ticket no Movidesk
    'protocol': Integer,           # Protocolo do ticket
    'subject': String(500),        # Assunto
    'category': String(255),       # Categoria
    'urgency': String(50),         # Urgência
    'status': String(50),          # Status
    'created_date': DateTime,      # Data de criação
    'organization_business_name': String(255),  # Nome da organização
    'owner_team': String(255),     # Time responsável
    'owner_name': String(255),     # Nome do responsável
    'actions_count': Integer,      # Número de ações
    'resolved_in': String(100),    # Tempo de resolução
    'created_at': DateTime,
    'updated_at': DateTime
}
```

## Tecnologias Utilizadas

- **Backend**: Flask 3.0.0
- **ORM**: SQLAlchemy 2.0.25
- **Migrations**: Alembic
- **Banco de Dados**: PostgreSQL (via psycopg2-binary)
- **Frontend**: TailwindCSS, Font Awesome, jQuery
- **Máscaras**: jQuery Mask Plugin
- **Integração**: API Movidesk
- **Autenticação**: JWT via Auth-Service
- **Ambiente**: python-dotenv

## Migrations

O projeto usa Alembic para gerenciamento de migrations do banco de dados.

### Comandos Úteis

```bash
# Verificar status das migrations
alembic current

# Ver histórico de migrations
alembic history

# Executar todas as migrations pendentes
alembic upgrade head

# Reverter última migration
alembic downgrade -1

# Reverter todas as migrations
alembic downgrade base

# Criar nova migration
alembic revision -m "descrição da mudança"
```

## Testes

O projeto inclui scripts de teste na pasta `test/`:

```bash
# Testar fluxo de login
python test/test_login_flow.py

# Testar todas as rotas
python test/test_all_routes.py
```

## Solução de Problemas

### Erro de Conexão com Banco de Dados

```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solução**: Verifique se o PostgreSQL está rodando e as credenciais no `.env` estão corretas.

### Erro ao Sincronizar Organizações

```
Erro: 401 Unauthorized
```

**Solução**: Verifique se o token do Movidesk no `.env` está correto e válido.

### Erro de Coluna Inexistente

```
psycopg2.errors.UndefinedColumn: column clients.billing_cycle_type does not exist
```

**Solução**: Execute as migrations: `alembic upgrade head`

### Auth-Service Não Conecta

```
Erro ao conectar no auth-service
```

**Solução**: Certifique-se de que o Auth-Service está rodando em `http://localhost:8000` e acessível.

## Suporte

Para dúvidas ou problemas, consulte a documentação ou entre em contato com a equipe de desenvolvimento.

## Licença

Proprietário - Todos os direitos reservados
