# App Financeiro - Sistema Completo

Sistema de gestão financeira com integração ao Movidesk para sincronização de organizações e gerenciamento de clientes.

## Funcionalidades Implementadas

### 1. Sistema de Integração com Movidesk
- Card "Integrações" no dashboard principal
- Tela de seleção de integrações disponíveis
- Tela de opções do Movidesk (Tickets e Organizações)
- Sistema de sincronização de organizações

### 2. Gerenciamento de Clientes
- Card "Tickets" (renomeado de Vendas) no dashboard
- Lista de clientes cadastrados
- Cadastro e edição de clientes
- Vinculação de clientes a organizações do Movidesk
- Validação e persistência em banco de dados

### 3. Sistema de Breadcrumbs
- Navegação hierárquica em todas as telas
- Macro reutilizável para breadcrumbs
- Integrado em todas as páginas do sistema

### 4. Banco de Dados
- PostgreSQL com SQLAlchemy
- Modelo de Organizations (organizações do Movidesk)
- Modelo de Clients (clientes do sistema)
- Relacionamento entre clientes e organizações
- Criação automática de tabelas na inicialização

## Estrutura do Projeto

```
app-financeiro/
├── app/
│   ├── controllers/
│   │   ├── auth/
│   │   ├── clients/
│   │   │   └── clients_controller.py
│   │   ├── dashboard/
│   │   └── integrations/
│   │       └── integrations_controller.py
│   ├── models/
│   │   ├── database.py
│   │   ├── organization.py
│   │   └── client.py
│   └── services/
│       ├── auth_service.py
│       ├── client_service.py
│       └── movidesk_service.py
├── templates/
│   ├── macros/
│   │   └── breadcrumbs.html
│   ├── clients/
│   │   ├── list.html
│   │   └── form.html
│   ├── integrations/
│   │   ├── list.html
│   │   ├── movidesk_options.html
│   │   ├── movidesk_organizations.html
│   │   └── movidesk_tickets.html
│   ├── base.html
│   ├── dashboard.html
│   └── login.html
├── static/
├── .env
├── config.py
├── routes.py
├── server.py
└── requirements.txt
```

## Configuração

### 1. Requisitos
- Python 3.8+
- PostgreSQL 12+

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

### 5. Inicializar o Sistema

```bash
python server.py
```

O sistema criará automaticamente as tabelas no banco de dados na primeira execução.

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
2. Clique no card "Tickets"
3. Clique em "Novo Cliente"
4. Preencha os dados do cliente
5. Selecione uma organização (opcional - requer sincronização prévia)
6. Clique em "Cadastrar Cliente"

### Navegação com Breadcrumbs

Todas as telas possuem breadcrumbs no topo para facilitar a navegação:
- Dashboard > Integrações > Movidesk > Organizações
- Dashboard > Tickets > Clientes > Novo Cliente

## Rotas da API

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

### Integrações

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/admin/integrations` | Lista integrações |
| GET | `/admin/integrations/movidesk` | Opções Movidesk |
| GET | `/admin/integrations/movidesk/organizations` | Tela sincronização |
| POST | `/admin/integrations/movidesk/organizations/sync` | Sincroniza organizações |
| GET | `/admin/integrations/movidesk/tickets` | Tela tickets (placeholder) |

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
    'organization_id': String(50), # FK para organizations
    'address': String(500),        # Endereço
    'city': String(100),           # Cidade
    'state': String(2),            # UF
    'zipcode': String(20),         # CEP
    'created_at': DateTime,
    'updated_at': DateTime
}
```

## Tecnologias Utilizadas

- **Backend**: Flask 3.0.0
- **ORM**: SQLAlchemy 2.0.25
- **Banco de Dados**: PostgreSQL (via psycopg2-binary)
- **Frontend**: TailwindCSS, Font Awesome
- **Integração**: API Movidesk
- **Ambiente**: python-dotenv

## Próximos Passos

1. **Sincronização de Tickets**: Implementar importação de tickets do Movidesk
2. **Dashboard de Tickets**: Criar visualização de tickets por cliente
3. **Filtros e Busca**: Adicionar busca avançada de clientes
4. **Paginação**: Implementar paginação nas listas
5. **Relatórios**: Criar relatórios de clientes e organizações
6. **Validações**: Adicionar validações de CPF/CNPJ
7. **Testes**: Criar testes automatizados

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

### Tabelas não Criadas

**Solução**: Certifique-se de que o banco de dados existe e o usuário tem permissões de criação de tabelas.

## Suporte

Para dúvidas ou problemas, consulte a documentação ou entre em contato com a equipe de desenvolvimento.

## Licença

Proprietário - Todos os direitos reservados
