# README - Migrations e Seeders

Sistema de gerenciamento de banco de dados seguindo o padrão Laravel.

## 📋 Índice

- [Estrutura do Banco de Dados](#estrutura-do-banco-de-dados)
- [Migrations](#migrations)
- [Seeders](#seeders)
- [Como Executar](#como-executar)
- [Comandos Úteis](#comandos-úteis)

---

## 🗄️ Estrutura do Banco de Dados

### Sistema de Usuários e Grupos (N:N)

#### `groups` (Tabela de Grupos)
- **id** - ID do grupo (PK)
- **name** - Nome do grupo
- **slug** - Slug único para URLs
- **description** - Descrição do grupo
- **color** - Cor de identificação (hex)
- **icon** - Ícone Font Awesome
- **permissions** - JSON com permissões
- **hierarchy_level** - Nível hierárquico (1=maior, 99=menor)
- **is_active** - Status ativo/inativo
- **created_at** - Data de criação
- **updated_at** - Data de atualização

**Grupos Padrão:**
1. Administradores (nível 1) - Acesso total
2. Gestores (nível 2) - Aprovação de viagens
3. Colaboradores (nível 3) - Usuários padrão
4. Visitantes (nível 4) - Somente leitura

#### `users` (Tabela de Usuários)
- **id** - ID do usuário (PK)
- **name** - Nome completo
- **email** - Email único
- **cpf** - CPF único
- **phone** - Telefone
- **avatar** - URL do avatar
- **is_active** - Status ativo/inativo
- **email_verified_at** - Data de verificação do email
- **last_login_at** - Data do último login
- **created_at** - Data de criação
- **updated_at** - Data de atualização

#### `user_groups` (Tabela Pivot - N:N)
Relaciona usuários com grupos (um usuário pode ter múltiplos grupos).

- **id** - ID do vínculo (PK)
- **user_id** - ID do usuário (FK → users.id)
- **group_id** - ID do grupo (FK → groups.id)
- **created_at** - Data do vínculo

**Constraints:**
- UNIQUE(user_id, group_id) - Um usuário não pode estar no mesmo grupo duas vezes
- CASCADE DELETE - Remove vínculo ao deletar usuário ou grupo

---

### Sistema de Viagens

#### `states` (Estados Brasileiros)
- **id** - ID do estado (PK)
- **name** - Nome do estado
- **uf** - Sigla (ex: RO, SP)
- **ibge_code** - Código IBGE
- **created_at** - Data de criação
- **updated_at** - Data de atualização

#### `cities` (Cidades)
- **id** - ID da cidade (PK)
- **name** - Nome da cidade
- **ibge_code** - Código IBGE (único)
- **state_id** - ID do estado (FK → states.id)
- **created_at** - Data de criação
- **updated_at** - Data de atualização

**Dados Iniciais:**
- Estado: Rondônia (RO)
- 52 cidades de Rondônia com códigos IBGE

#### `travels` (Viagens)
- **id** - ID da viagem (PK)
- **user_id** - ID do usuário (FK → users.id)
- **city_id** - ID da cidade destino (FK → cities.id)
- **purpose** - Motivo da viagem
- **description** - Descrição detalhada
- **departure_date** - Data/hora de saída
- **return_date** - Data/hora de retorno
- **status** - Status (ENUM)
- **approved_by** - ID do aprovador (FK → users.id)
- **approved_at** - Data de aprovação
- **notes** - Observações
- **admin_notes** - Notas administrativas
- **created_at** - Data de criação
- **updated_at** - Data de atualização

**Status Disponíveis:**
- `PENDING` - Pendente de aprovação
- `APPROVED` - Aprovada
- `IN_PROGRESS` - Em andamento
- `COMPLETED` - Concluída
- `CANCELLED` - Cancelada

---

### Sistema de Clientes e Tickets

#### `organizations` (Organizações do Movidesk)
- **id** - ID da organização (PK, String)
- **business_name** - Nome da empresa
- **person_type** - Tipo de pessoa
- **is_active** - Status ativo/inativo
- **created_at** - Data de criação
- **updated_at** - Data de atualização

#### `clients` (Clientes)
- **id** - ID do cliente (PK)
- **name** - Nome do cliente
- **email** - Email
- **phone** - Telefone
- **document** - CNPJ/CPF (único)
- **organization_id** - ID da organização (FK → organizations.id)
- **address** - Endereço
- **city** - Cidade
- **state** - Estado (UF)
- **zipcode** - CEP
- **billing_cycle** - Ciclo de cobrança
- **billing_day** - Dia de cobrança
- **created_at** - Data de criação
- **updated_at** - Data de atualização

#### `client_organizations` (Pivot - N:N)
Relaciona clientes com organizações.

- **id** - ID do vínculo (PK)
- **client_id** - ID do cliente (FK → clients.id)
- **organization_id** - ID da organização (FK → organizations.id)
- **created_at** - Data do vínculo

#### `tickets` (Tickets de Atendimento)
- **id** - ID do ticket (PK)
- **subject** - Assunto
- **status** - Status do ticket
- **category** - Categoria (Incidente, Dúvida, etc)
- **service_full** - Serviço completo
- **organization_name** - Nome da organização
- **client_name** - Nome do cliente
- **owner_name** - Responsável
- **created_by_name** - Criado por (nome)
- **created_by_email** - Criado por (email)
- **created_date** - Data de criação
- **resolved_in** - Data de resolução (encerramento do chat)
- **closed_in** - Data de fechamento oficial
- **custom_field_module** - Módulo customizado
- **synced_at** - Data de sincronização

#### `sync_logs` (Logs de Sincronização)
- **id** - ID do log (PK)
- **sync_type** - Tipo de sincronização
- **total** - Total de registros
- **synced** - Registros sincronizados
- **updated** - Registros atualizados
- **errors** - Quantidade de erros
- **synced_at** - Data da sincronização

---

## 📦 Migrations

Todas as migrations seguem o padrão Laravel: **uma tabela por arquivo**.

### Ordem de Execução:

```
001_create_groups_table.py              → Grupos de usuários
002_create_users_table.py               → Usuários
003_create_user_groups_table.py         → Pivot users ↔ groups
004_create_states_table.py              → Estados
005_create_cities_table.py              → Cidades
006_create_travels_table.py             → Viagens
007_create_organizations_table.py       → Organizações
008_create_clients_table.py             → Clientes
009_create_client_organizations_table.py → Pivot clients ↔ organizations
010_create_sync_logs_table.py           → Logs de sincronização
011_create_tickets_table.py             → Tickets
```

### Características:

- ✅ Nomenclatura descritiva: `XXX_create_TABELA_table.py`
- ✅ Prefixos numéricos (001-011) para ordem de execução
- ✅ Métodos `upgrade()` e `downgrade()` completos
- ✅ Timestamps timezone-aware em todas as tabelas
- ✅ Índices criados e removidos corretamente
- ✅ Foreign keys com constraints adequadas
- ✅ Cascade delete nas tabelas pivot

---

## 🌱 Seeders

### Seeders Disponíveis:

#### 1. `groups_seeder.py`
Cria 4 grupos de usuários:
- Administradores (hierarquia 1)
- Gestores (hierarquia 2)
- Colaboradores (hierarquia 3)
- Visitantes (hierarquia 4)

Cada grupo possui:
- Permissões JSON detalhadas
- Cor e ícone personalizados
- Nível hierárquico

#### 2. `users_seeder.py`
Cria 5 usuários de teste:
- 1 Administrador
- 1 Gestor
- 3 Colaboradores

**Usuários criados:**
- admin@bettertech.com.br
- gestor@bettertech.com.br
- maria.silva@bettertech.com.br
- joao.santos@bettertech.com.br
- ana.costa@bettertech.com.br

**Importante:** Este seeder também cria os vínculos na tabela pivot `user_groups`.

#### 3. `cities_seeder.py`
Popula o banco com:
- Estado de Rondônia (RO)
- 52 cidades de Rondônia com códigos IBGE

#### 4. `database_seeder.py` (Master)
Executa todos os seeders na ordem correta:
1. Groups
2. Users (+ vínculos user_groups)
3. Cities

---

## 🚀 Como Executar

### 1. Resetar Banco de Dados (Opcional)

```bash
# Via SQL (pgAdmin ou psql)
DELETE FROM alembic_version;
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

### 2. Executar Migrations

```bash
cd C:\Python\bettertech\app-financeiro

# Verificar status atual
alembic current

# Executar todas as migrations
alembic upgrade head

# Verificar se aplicou corretamente
alembic current
# Deve mostrar: 011
```

### 3. Executar Seeders

**Opção 1: Executar todos de uma vez (Recomendado)**
```bash
python database/seeders/database_seeder.py
```

**Opção 2: Executar individualmente**
```bash
# Ordem obrigatória:
python database/seeders/groups_seeder.py
python database/seeders/users_seeder.py
python database/seeders/cities_seeder.py
```

### 4. Iniciar Servidor

```bash
python server.py
```

Acesse: http://127.0.0.1:5000

---

## 🛠️ Comandos Úteis

### Alembic (Migrations)

```bash
# Ver status atual
alembic current

# Ver histórico de migrations
alembic history

# Upgrade para versão específica
alembic upgrade 005

# Downgrade para versão anterior
alembic downgrade -1

# Downgrade para versão específica
alembic downgrade 003

# Downgrade completo
alembic downgrade base

# Criar nova migration (apenas se necessário)
alembic revision -m "descricao_da_mudanca"
```

### Verificar Banco de Dados

```sql
-- Ver todas as tabelas criadas
SELECT tablename FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;

-- Ver quantidade de registros por tabela
SELECT 'groups' as tabela, COUNT(*) FROM groups
UNION ALL
SELECT 'users', COUNT(*) FROM users
UNION ALL
SELECT 'user_groups', COUNT(*) FROM user_groups
UNION ALL
SELECT 'states', COUNT(*) FROM states
UNION ALL
SELECT 'cities', COUNT(*) FROM cities
UNION ALL
SELECT 'travels', COUNT(*) FROM travels;

-- Ver usuários e seus grupos
SELECT
    u.id,
    u.name,
    u.email,
    g.name as grupo
FROM users u
JOIN user_groups ug ON u.id = ug.user_id
JOIN groups g ON ug.group_id = g.id
ORDER BY u.id;
```

---

## 📊 Diagrama de Relacionamentos

```
groups ←→ user_groups ←→ users
                          ↓
                        travels
                          ↓
                        cities → states

organizations ←→ client_organizations ←→ clients

tickets (independente)
sync_logs (independente)
```

---

## ⚠️ Observações Importantes

1. **Ordem de Execução:** Sempre execute as migrations na ordem numérica (001 → 011)
2. **Seeders:** Execute os seeders APÓS as migrations
3. **Dependências:**
   - `users_seeder` depende de `groups_seeder`
   - `cities_seeder` cria automaticamente o estado de Rondônia
4. **Tabelas Pivot:**
   - `user_groups` - Relacionamento N:N entre users e groups
   - `client_organizations` - Relacionamento N:N entre clients e organizations
5. **Timezone:** Todos os timestamps usam timezone-aware (PostgreSQL)
6. **Índices:** Criados automaticamente em colunas únicas e foreign keys
7. **Cascade Delete:** Tabelas pivot usam CASCADE ao deletar registros relacionados

---

## 📝 Estrutura de Pastas

```
app-financeiro/
├── database/
│   ├── migrations/
│   │   ├── versions/
│   │   │   ├── 001_create_groups_table.py
│   │   │   ├── 002_create_users_table.py
│   │   │   ├── 003_create_user_groups_table.py
│   │   │   ├── ... (até 011)
│   │   └── env.py
│   └── seeders/
│       ├── groups_seeder.py
│       ├── users_seeder.py
│       ├── cities_seeder.py
│       └── database_seeder.py
├── app/
│   └── models/
│       ├── group.py
│       ├── user.py
│       ├── user_group.py (Table pivot)
│       ├── state.py
│       ├── city.py
│       ├── travel.py
│       ├── organization.py
│       ├── client.py
│       ├── ticket.py
│       └── sync_log.py
└── README_MIGRATIONS.md (este arquivo)
```

---

## 🎯 Resultado Final

Após executar migrations e seeders:

- ✅ **11 Tabelas** criadas
- ✅ **4 Grupos** cadastrados
- ✅ **5 Usuários** cadastrados
- ✅ **5 Vínculos** user-group criados
- ✅ **1 Estado** (Rondônia)
- ✅ **52 Cidades** de Rondônia
- ✅ Sistema pronto para uso!

---

**Desenvolvido seguindo o padrão Laravel de migrations e seeders.**

Data: 2025-10-11
