# App Financeiro - Sistema de Gestão Empresarial

Sistema completo de gestão empresarial com integração ao Movidesk para sincronização de organizações, gerenciamento de clientes, tickets, controle de frota e muito mais.

## Funcionalidades Principais

### 1. Sistema de Autenticação e Autorização
- Integração com Auth-Service (microserviço de autenticação)
- Login com JWT tokens
- Proteção de rotas com middleware de autenticação
- Sistema de grupos e permissões granulares
- Gerenciamento de usuários com níveis de acesso

### 2. Integração com Movidesk
- Sincronização automática de organizações
- Sincronização de tickets do Movidesk
- Vinculação múltipla de clientes a organizações
- Gerenciamento de status de organizações
- Histórico de sincronizações com logs detalhados

### 3. Gerenciamento de Clientes
- Cadastro completo com validação de CPF/CNPJ
- Interface organizada em tabs:
  - **Pessoa**: Dados básicos e vinculação com Movidesk
  - **Cobrança**: Configuração de ciclos (fixo ou mensal)
  - **Endereços**: Localização completa com CEP
  - **Módulos**: Controle de módulos contratados
  - **Contatos**: Pessoas de contato vinculadas
- Sistema de busca e filtros avançados
- Vinculação múltipla com organizações do Movidesk

### 4. Sistema de Tickets
- Visualização de tickets por cliente e organização
- Integração em tempo real com API do Movidesk
- Filtros avançados por status, categoria e urgência
- Relatórios de tickets em PDF
- Dashboard com métricas de atendimento

### 5. Gerenciamento de Frota (Veículos)
- Cadastro completo de veículos da frota
- Controle de status ativo/inativo
- Sistema de manutenções periódicas configuráveis
- Configuração de intervalos de manutenção por tipo
- Histórico de viagens por veículo
- Controle de quilometragem
- Metadados calculados automaticamente

### 6. Sistema de Viagens
- Solicitação de viagens
- Aprovação de viagens com workflow
- Controle por estado e cidade
- Histórico completo de viagens

### 7. Sistema de Licenças
- Gerenciamento de licenças de software
- Upload de licenças em lote
- Geração de relatórios em PDF
- Controle de módulos por licença
- Visualização de datas de vencimento

### 8. Perfil e Notificações
- Gerenciamento de perfil do usuário
- Sistema de notificações em tempo real
- Central de notificações com contador
- Marcação de leitura individual ou em massa
- Histórico de atividades

### 9. Configurações do Sistema
- Parâmetros configuráveis por módulo
- Interface intuitiva para ajustes
- Controle de integrações
- Logs de auditoria

### 10. Sistema de Navegação
- Breadcrumbs em todas as páginas
- Menu lateral responsivo
- Dashboard com cards informativos
- Interface moderna com TailwindCSS

## Estrutura do Projeto

```
app-financeiro/
├── app/
│   ├── controllers/
│   │   ├── auth/
│   │   ├── clients/
│   │   ├── dashboard/
│   │   ├── groups/
│   │   ├── integrations/
│   │   ├── licenses/
│   │   ├── permissions/
│   │   ├── reports/
│   │   ├── settings/
│   │   ├── tickets/
│   │   ├── users/
│   │   ├── vehicles/
│   │   ├── notes_controller.py
│   │   ├── notifications_controller.py
│   │   ├── profile_controller.py
│   │   └── travels_controller.py
│   ├── models/
│   │   ├── application.py
│   │   ├── city.py
│   │   ├── client.py
│   │   ├── client_application.py
│   │   ├── client_contact.py
│   │   ├── client_organization.py
│   │   ├── database.py
│   │   ├── group.py
│   │   ├── license.py
│   │   ├── license_date.py
│   │   ├── license_module.py
│   │   ├── maintenance_type.py
│   │   ├── note.py
│   │   ├── notification.py
│   │   ├── organization.py
│   │   ├── parameter.py
│   │   ├── permission.py
│   │   ├── state.py
│   │   ├── sync_log.py
│   │   ├── ticket.py
│   │   ├── travel.py
│   │   ├── user.py
│   │   ├── user_group.py
│   │   ├── vehicle.py
│   │   ├── vehicle_maintenance_config.py
│   │   ├── vehicle_maintenance_history.py
│   │   ├── vehicle_meta.py
│   │   └── vehicle_travel_history.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── client_service.py
│   │   ├── movidesk_service.py
│   │   └── ticket_service.py
│   └── utils/
│       └── permissions_helper.py
├── database/
│   ├── migrations/
│   │   └── versions/
│   │       └── (32 migrations)
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
│   │   ├── clients/
│   │   ├── groups/
│   │   ├── integrations/
│   │   ├── licenses/
│   │   ├── notes/
│   │   ├── notifications/
│   │   ├── permissions/
│   │   ├── profile/
│   │   ├── reports/
│   │   ├── settings/
│   │   ├── tickets/
│   │   ├── travels/
│   │   ├── users/
│   │   ├── vehicles/
│   │   └── dashboard.html
│   └── base.html
├── static/
│   └── css/
│       └── dashboard.css
├── .env
├── .gitignore
├── alembic.ini
├── config.py
├── routes.py
├── main.py
├── requirements.txt
└── README.md
```

## Requisitos do Sistema

- **Python**: 3.8 ou superior
- **Banco de Dados**: PostgreSQL 12 ou superior
- **Auth-Service**: Microserviço de autenticação rodando
- **Memória**: Mínimo 2GB RAM
- **Espaço em Disco**: Mínimo 1GB

## Instalação

### 1. Clonar o Repositório

```bash
cd app-financeiro
```

### 2. Criar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Banco de Dados

Criar banco de dados PostgreSQL:

```sql
CREATE DATABASE app_financeiro;
CREATE USER app_financeiro_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE app_financeiro TO app_financeiro_user;
```

### 5. Configurar Variáveis de Ambiente

Criar arquivo `.env` na raiz do projeto:

```env
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-very-secure-random-secret-key-here

# Auth Service Configuration
AUTH_SERVICE_URL=http://your-auth-service-url:8000
AUTH_SERVICE_TIMEOUT=10

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256

# Database Configuration
DB_USER=app_financeiro_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=app_financeiro

# Movidesk API Configuration
MOVIDESK_TOKEN=your-movidesk-api-token-here
```

**Importante**: Substitua todos os valores de exemplo por valores reais e seguros.

### 6. Executar Migrations

```bash
# Executar todas as migrations
alembic upgrade head
```

### 7. Popular Dados Iniciais (Opcional)

```bash
# Popular grupos, usuários e cidades
python database/seeders/database_seeder.py
```

### 8. Inicializar o Sistema

```bash
python main.py
```

O sistema estará disponível em `http://localhost:5000`

## Configuração para Produção

### Segurança

1. **Alterar SECRET_KEY**: Gere uma chave aleatória segura
2. **Desabilitar DEBUG**: `FLASK_DEBUG=False`
3. **Usar HTTPS**: Configure certificado SSL/TLS
4. **Firewall**: Proteja a porta do banco de dados
5. **Senhas**: Use senhas fortes e únicas

### Performance

1. **Usar servidor WSGI**: Gunicorn ou uWSGI
2. **Configurar proxy reverso**: Nginx ou Apache
3. **Habilitar cache**: Redis ou Memcached
4. **Otimizar queries**: Índices no banco de dados

### Backup

1. **Banco de Dados**: Backup diário automático
2. **Arquivos**: Backup de uploads e logs
3. **Configurações**: Versionamento de `.env`

### Monitoramento

1. **Logs**: Configurar sistema de logs centralizado
2. **Métricas**: Monitorar uso de recursos
3. **Alertas**: Notificações de erros críticos

## Rotas Principais da API

### Autenticação
- `GET /` - Página inicial (redireciona para login ou dashboard)
- `GET/POST /login` - Login no sistema
- `GET /logout` - Logout

### Dashboard
- `GET /admin/dashboard` - Dashboard principal

### Clientes
- `GET /admin/clients` - Lista de clientes
- `GET /admin/clients/new` - Novo cliente
- `POST /admin/clients/create` - Criar cliente
- `GET /admin/clients/<id>/edit` - Editar cliente
- `POST /admin/clients/<id>/update` - Atualizar cliente
- `POST /admin/clients/<id>/delete` - Remover cliente

### Veículos
- `GET /admin/vehicles` - Lista de veículos
- `GET /admin/vehicles/new` - Novo veículo
- `POST /admin/vehicles/create` - Criar veículo
- `GET /admin/vehicles/<id>` - Detalhes do veículo
- `GET /admin/vehicles/<id>/edit` - Editar veículo
- `POST /admin/vehicles/<id>/update` - Atualizar veículo
- `POST /admin/vehicles/<id>/toggle-status` - Ativar/Inativar veículo
- `POST /admin/vehicles/<id>/maintenance-configs` - Adicionar config. de manutenção
- `DELETE /admin/vehicles/<id>/maintenance-configs/<config_id>` - Remover config. de manutenção

### Tickets
- `GET /admin/tickets` - Lista de tickets
- `GET /admin/tickets/client/<id>` - Tickets por cliente
- `GET /admin/tickets/client/<id>/report/pdf` - Relatório PDF

### Integrações
- `GET /admin/integrations` - Lista de integrações
- `GET /admin/integrations/movidesk` - Opções Movidesk
- `GET /admin/integrations/movidesk/organizations` - Organizações
- `POST /admin/integrations/movidesk/organizations/sync` - Sincronizar organizações
- `GET /admin/integrations/movidesk/tickets` - Tickets Movidesk
- `POST /admin/integrations/movidesk/tickets/sync` - Sincronizar tickets

### Usuários e Permissões
- `GET /admin/users` - Lista de usuários
- `GET /admin/groups` - Lista de grupos
- `GET /admin/permissions` - Gerenciar permissões
- `GET /admin/permissions/groups` - Permissões por grupo

### Licenças
- `GET /admin/licenses` - Lista de licenças
- `GET /admin/licenses/upload` - Upload de licenças
- `GET /admin/licenses/generate` - Gerar licença
- `GET /admin/licenses/view-pdf` - Visualizar PDF

### Viagens
- `GET /admin/travels` - Lista de viagens
- `GET /admin/travels/new` - Nova viagem
- `POST /admin/travels/create` - Criar viagem
- `GET /admin/travels/<id>/approve` - Aprovar viagem
- `GET /admin/travels/<id>/cancel` - Cancelar viagem

### Notificações
- `GET /admin/notifications` - Central de notificações
- `GET /admin/api/notifications` - Lista de notificações (API)
- `GET /admin/api/notifications/unread-count` - Contador de não lidas
- `POST /admin/api/notifications/<id>/read` - Marcar como lida
- `POST /admin/api/notifications/read-all` - Marcar todas como lidas

### Perfil
- `GET /admin/profile` - Visualizar perfil
- `POST /admin/profile/update` - Atualizar perfil

### Configurações
- `GET /admin/settings` - Configurações do sistema
- `POST /admin/settings/<id>/update` - Atualizar parâmetro

## Tecnologias Utilizadas

### Backend
- **Flask** 3.1.2 - Framework web
- **SQLAlchemy** 2.0.44 - ORM
- **Alembic** 1.17.0 - Sistema de migrations
- **psycopg** 3.2.3 - Driver PostgreSQL (versão 3)
- **python-dotenv** 1.1.1 - Gerenciamento de variáveis de ambiente
- **requests** 2.32.5 - Cliente HTTP

### Frontend
- **TailwindCSS** - Framework CSS
- **Font Awesome** - Ícones
- **jQuery** - Manipulação DOM
- **jQuery Mask Plugin** - Máscaras de input

### Segurança
- **JWT** - Autenticação e autorização
- **bcrypt** - Hash de senhas (via Auth-Service)
- **CSRF Protection** - Proteção contra CSRF

### Integrações
- **Movidesk API** - Sincronização de tickets e organizações
- **Auth-Service** - Microserviço de autenticação

## Comandos Úteis do Alembic

```bash
# Ver status atual
alembic current

# Ver histórico de migrations
alembic history

# Executar migrations pendentes
alembic upgrade head

# Reverter última migration
alembic downgrade -1

# Reverter todas as migrations
alembic downgrade base

# Criar nova migration
alembic revision -m "descrição da mudança"
```

## Solução de Problemas Comuns

### Erro de Conexão com Banco de Dados

```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solução**:
- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no arquivo `.env`
- Teste a conexão: `psql -U app_financeiro_user -d app_financeiro`

### Erro ao Sincronizar com Movidesk

```
Erro: 401 Unauthorized
```

**Solução**:
- Verifique se o token do Movidesk está correto
- Confirme se o token tem as permissões necessárias
- Teste o token diretamente na API do Movidesk

### Erro de Coluna Inexistente

```
psycopg.errors.UndefinedColumn: column does not exist
```

**Solução**:
- Execute todas as migrations: `alembic upgrade head`
- Verifique o status: `alembic current`

### Auth-Service Não Conecta

```
Erro ao conectar no auth-service
```

**Solução**:
- Certifique-se de que o Auth-Service está rodando
- Verifique a URL no arquivo `.env`
- Teste a conectividade: `curl http://auth-service-url:8000/health`

### Erro de Permissão

```
403 Forbidden - Você não tem permissão para acessar esta página
```

**Solução**:
- Verifique se o usuário está no grupo correto
- Confirme as permissões do grupo em `/admin/permissions`
- Execute o seeder de permissões se necessário

## Manutenção

### Limpeza de Logs

```bash
# Limpar logs antigos (implementar conforme necessário)
find logs/ -name "*.log" -mtime +30 -delete
```

### Atualização do Sistema

```bash
# Atualizar código
git pull origin main

# Atualizar dependências
pip install -r requirements.txt --upgrade

# Executar novas migrations
alembic upgrade head

# Reiniciar aplicação
systemctl restart app-financeiro
```

### Backup do Banco de Dados

```bash
# Backup completo
pg_dump -U app_financeiro_user app_financeiro > backup_$(date +%Y%m%d).sql

# Restaurar backup
psql -U app_financeiro_user app_financeiro < backup_20240101.sql
```

## Boas Práticas

1. **Sempre testar em ambiente de desenvolvimento** antes de deploy em produção
2. **Fazer backup** antes de executar migrations
3. **Documentar mudanças** em commits claros e descritivos
4. **Monitorar logs** regularmente para identificar problemas
5. **Manter dependências atualizadas** com patches de segurança
6. **Revisar permissões** periodicamente
7. **Auditar acessos** e atividades suspeitas

## Suporte

Para dúvidas técnicas ou problemas:
1. Consulte este README
2. Verifique os logs da aplicação
3. Entre em contato com a equipe de desenvolvimento

## Licença

Proprietário - Todos os direitos reservados © 2024
