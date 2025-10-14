# 🔐 Sistema de Permissões - App Financeiro

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura](#arquitetura)
3. [Instalação e Configuração](#instalação-e-configuração)
4. [Permissões Disponíveis](#permissões-disponíveis)
5. [Como Usar](#como-usar)
6. [Exemplos Práticos](#exemplos-práticos)
7. [API Reference](#api-reference)

---

## 🎯 Visão Geral

O sistema de permissões implementado permite controle granular de acesso às funcionalidades do sistema através de:

- **Permissões**: Ações específicas que podem ser realizadas (ex: `viagens_create`, `tickets_view`)
- **Grupos**: Conjuntos de permissões atribuídos a usuários (ex: Administrador, Gerente, Colaborador)
- **Usuários**: Podem pertencer a múltiplos grupos e herdam todas as permissões desses grupos

### Características Principais

✅ **Granularidade**: Controle fino sobre cada funcionalidade
✅ **Flexibilidade**: Usuários podem ter múltiplos grupos
✅ **Herança**: Permissões herdadas de todos os grupos do usuário
✅ **Decorators**: Proteção fácil de rotas com decorators Python
✅ **Templates**: Controle de exibição de elementos na interface
✅ **API REST**: Gerenciamento via API

---

## 🏗️ Arquitetura

### Estrutura de Banco de Dados

```
users ←→ user_groups ←→ groups ←→ group_permissions ←→ permissions
```

#### Tabelas

**permissions**
- `id`: ID da permissão
- `name`: Nome legível (ex: "Visualizar Viagens")
- `slug`: Identificador único (ex: "viagens_view")
- `description`: Descrição da permissão
- `module`: Módulo ao qual pertence (ex: "viagens")

**group_permissions** (tabela pivot)
- `id`: ID do relacionamento
- `group_id`: ID do grupo
- `permission_id`: ID da permissão

**groups** (já existente)
- Relacionamento many-to-many com `permissions` através de `group_permissions`

**users** (já existente)
- Relacionamento many-to-many com `groups` através de `user_groups`

---

## 🚀 Instalação e Configuração

### Passo 1: Executar Migrations

```bash
cd app-financeiro
python main.py --migrate
```

Isso criará as tabelas:
- `permissions`
- `group_permissions`

### Passo 2: Popular Permissões

```bash
python database/seeders/permissions_seeder.py
```

Isso criará **todas as 67 permissões** do sistema organizadas por módulo.

### Passo 3: Associar Permissões aos Grupos

Acesse a interface administrativa:
```
http://localhost:5000/admin/permissions/groups
```

Ou execute via API/Python:

```python
from app.models.database import SessionLocal
from app.models.group import Group
from app.models.permission import Permission

db = SessionLocal()

# Buscar grupo admin
admin_group = db.query(Group).filter(Group.slug == 'admin').first()

# Buscar permissões
permissions = db.query(Permission).all()

# Associar todas as permissões ao grupo admin
admin_group.permissions_rel = permissions
db.commit()
```

---

## 📚 Permissões Disponíveis

### Dashboard (1 permissão)
- `dashboard_view` - Visualizar Dashboard

### Clientes (5 permissões)
- `clients_view` - Visualizar Clientes
- `clients_create` - Criar Cliente
- `clients_edit` - Editar Cliente
- `clients_delete` - Deletar Cliente
- `clients_manage_applications` - Gerenciar Aplicações de Clientes

### Tickets (6 permissões)
- `tickets_view` - Visualizar Tickets
- `tickets_view_client` - Visualizar Tickets de Cliente
- `tickets_create` - Criar Ticket
- `tickets_edit` - Editar Ticket
- `tickets_delete` - Deletar Ticket
- `tickets_manage_all` - Gerenciar Todos os Tickets

### Viagens (7 permissões)
- `viagens_view` - Visualizar Viagens
- `viagens_create` - Solicitar Viagem
- `viagens_edit` - Editar Viagem
- `viagens_delete` - Deletar Viagem
- `viagens_approve` - Aprovar Viagens
- `viagens_cancel` - Cancelar Viagens
- `viagens_view_all` - Visualizar Todas Viagens

### Integrações (6 permissões)
- `integrations_view` - Visualizar Integrações
- `integrations_manage` - Gerenciar Integrações
- `integrations_sync_tickets` - Sincronizar Tickets Movidesk
- `integrations_sync_organizations` - Sincronizar Organizações Movidesk
- `integrations_edit_organizations` - Editar Organizações
- `integrations_link_clients` - Vincular Clientes

### Licenças (7 permissões)
- `licenses_view` - Visualizar Licenças
- `licenses_upload` - Upload de Licenças
- `licenses_generate` - Gerar Licenças
- `licenses_generate_bulk` - Gerar Licenças em Lote
- `licenses_view_pdf` - Visualizar PDF de Licenças
- `licenses_delete_date` - Deletar Data de Licença
- `licenses_manage_modules` - Gerenciar Módulos de Licenças

### Usuários (5 permissões)
- `users_view` - Visualizar Usuários
- `users_create` - Criar Usuário
- `users_edit` - Editar Usuário
- `users_delete` - Deletar Usuário
- `users_manage_groups` - Gerenciar Grupos de Usuários

### Perfil (2 permissões)
- `profile_view` - Visualizar Próprio Perfil
- `profile_edit` - Editar Próprio Perfil

### Notificações (2 permissões)
- `notifications_view` - Visualizar Notificações
- `notifications_manage` - Gerenciar Notificações

### Configurações (2 permissões)
- `settings_view` - Visualizar Configurações
- `settings_edit` - Editar Configurações

### Notas (4 permissões)
- `notes_view` - Visualizar Notas
- `notes_create` - Criar Nota
- `notes_edit` - Editar Nota
- `notes_delete` - Deletar Nota

### Relatórios (3 permissões)
- `reports_view` - Visualizar Relatórios
- `reports_generate` - Gerar Relatórios
- `reports_export` - Exportar Relatórios

### Permissões (2 permissões)
- `permissions_view` - Visualizar Permissões
- `permissions_manage` - Gerenciar Permissões

### Grupos (4 permissões)
- `groups_view` - Visualizar Grupos
- `groups_create` - Criar Grupo
- `groups_edit` - Editar Grupo
- `groups_delete` - Deletar Grupo

---

## 🔨 Como Usar

### 1. Proteger Rotas com Decorators

#### Uma permissão específica

```python
from app.utils.permissions_helper import permission_required

@permission_required('viagens_create')
def create_travel():
    # Usuário precisa ter permissão viagens_create
    return render_template('travels/create.html')
```

#### Pelo menos uma permissão (OR)

```python
from app.utils.permissions_helper import any_permission_required

@any_permission_required(['viagens_view', 'viagens_view_all'])
def list_travels():
    # Usuário precisa ter viagens_view OU viagens_view_all
    return render_template('travels/list.html')
```

#### Todas as permissões (AND)

```python
from app.utils.permissions_helper import all_permissions_required

@all_permissions_required(['users_view', 'users_edit'])
def edit_user(user_id):
    # Usuário precisa ter viagens_view E viagens_edit
    return render_template('users/edit.html')
```

### 2. Verificar Permissões no Código Python

```python
from app.utils.permissions_helper import user_has_permission, get_current_user

# Verificar uma permissão
if user_has_permission('viagens_approve'):
    # Usuário pode aprovar viagens
    pass

# Obter usuário e verificar
user = get_current_user()
if user and user.has_permission('tickets_manage_all'):
    # Mostrar todos os tickets
    pass

# Verificar múltiplas permissões
if user.has_any_permission(['viagens_view', 'viagens_view_all']):
    # Usuário pode ver algum tipo de viagem
    pass
```

### 3. Controlar Exibição nos Templates

```html
<!-- Mostrar botão apenas se usuário tiver permissão -->
{% if 'viagens_create' in user_permissions %}
<a href="{{ url_for('admin.travels_create') }}" class="btn btn-primary">
    <i class="fas fa-plus"></i> Nova Viagem
</a>
{% endif %}

<!-- Mostrar menu apenas para usuários com permissão -->
{% if 'users_view' in user_permissions %}
<li class="nav-item">
    <a class="nav-link" href="{{ url_for('admin.users_list') }}">
        <i class="fas fa-users"></i> Usuários
    </a>
</li>
{% endif %}

<!-- Verificar múltiplas permissões -->
{% if 'tickets_edit' in user_permissions or 'tickets_delete' in user_permissions %}
<div class="actions">
    <!-- Ações de edição/exclusão -->
</div>
{% endif %}
```

### 4. Métodos do Model User

```python
user = User.query.get(1)

# Verificar uma permissão
user.has_permission('viagens_create')  # True ou False

# Verificar pelo menos uma permissão
user.has_any_permission(['viagens_view', 'viagens_view_all'])

# Verificar todas as permissões
user.has_all_permissions(['users_view', 'users_edit'])

# Obter todas as permissões do usuário
permissions = user.get_all_permissions()
# Retorna: ['viagens_view', 'viagens_create', 'tickets_view', ...]

# Verificar se pertence a um grupo
user.is_in_group('admin')  # True ou False
```

---

## 💡 Exemplos Práticos

### Exemplo 1: Atualizar rota de viagens existente

**Antes:**
```python
@admin_bp.route('/travels')
def travels_list():
    # Qualquer usuário autenticado pode acessar
    return render_template('travels/list.html')
```

**Depois:**
```python
from app.utils.permissions_helper import any_permission_required

@admin_bp.route('/travels')
@any_permission_required(['viagens_view', 'viagens_view_all'])
def travels_list():
    user = get_current_user()

    # Se usuário tem viagens_view_all, mostra todas
    if user.has_permission('viagens_view_all'):
        travels = Travel.query.all()
    else:
        # Senão, mostra apenas as suas
        travels = Travel.query.filter_by(user_id=user.id).all()

    return render_template('travels/list.html', travels=travels)
```

### Exemplo 2: Botões condicionais no template

```html
<!-- templates/admin/travels/list.html -->

<div class="card">
    <div class="card-header">
        <h3>Viagens</h3>

        <!-- Botão de criar aparece apenas para quem pode criar -->
        {% if 'viagens_create' in user_permissions %}
        <a href="{{ url_for('admin.travels_create') }}" class="btn btn-primary">
            <i class="fas fa-plus"></i> Nova Viagem
        </a>
        {% endif %}
    </div>

    <div class="card-body">
        <table class="table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Destino</th>
                    <th>Data</th>
                    <th>Status</th>
                    {% if 'viagens_edit' in user_permissions or 'viagens_delete' in user_permissions or 'viagens_approve' in user_permissions %}
                    <th>Ações</th>
                    {% endif %}
                </tr>
            </thead>
            <tbody>
                {% for travel in travels %}
                <tr>
                    <td>{{ travel.id }}</td>
                    <td>{{ travel.destination }}</td>
                    <td>{{ travel.travel_date }}</td>
                    <td>{{ travel.status }}</td>
                    {% if 'viagens_edit' in user_permissions or 'viagens_delete' in user_permissions or 'viagens_approve' in user_permissions %}
                    <td>
                        {% if 'viagens_edit' in user_permissions %}
                        <a href="{{ url_for('admin.travels_edit', travel_id=travel.id) }}"
                           class="btn btn-sm btn-info">
                            <i class="fas fa-edit"></i>
                        </a>
                        {% endif %}

                        {% if 'viagens_approve' in user_permissions and travel.status == 'pending' %}
                        <a href="{{ url_for('admin.travels_approve', travel_id=travel.id) }}"
                           class="btn btn-sm btn-success">
                            <i class="fas fa-check"></i>
                        </a>
                        {% endif %}

                        {% if 'viagens_delete' in user_permissions %}
                        <a href="{{ url_for('admin.travels_delete', travel_id=travel.id) }}"
                           class="btn btn-sm btn-danger"
                           onclick="return confirm('Deseja realmente deletar?')">
                            <i class="fas fa-trash"></i>
                        </a>
                        {% endif %}
                    </td>
                    {% endif %}
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
```

### Exemplo 3: Configurar permissões para diferentes perfis

```python
# Script para configurar permissões de grupos

from app.models.database import SessionLocal
from app.models.group import Group
from app.models.permission import Permission

db = SessionLocal()

# === GRUPO: ADMINISTRADOR (todas as permissões) ===
admin_group = db.query(Group).filter(Group.slug == 'admin').first()
all_permissions = db.query(Permission).all()
admin_group.permissions_rel = all_permissions

# === GRUPO: GERENTE (permissões de visualização e aprovação) ===
manager_group = db.query(Group).filter(Group.slug == 'gerente').first()
manager_permissions = db.query(Permission).filter(
    Permission.slug.in_([
        'dashboard_view',
        'viagens_view_all',
        'viagens_approve',
        'viagens_cancel',
        'tickets_view',
        'tickets_view_client',
        'clients_view',
        'reports_view',
        'reports_generate',
        'reports_export',
        'users_view'
    ])
).all()
manager_group.permissions_rel = manager_permissions

# === GRUPO: COLABORADOR (permissões básicas) ===
collab_group = db.query(Group).filter(Group.slug == 'colaborador').first()
collab_permissions = db.query(Permission).filter(
    Permission.slug.in_([
        'dashboard_view',
        'viagens_view',
        'viagens_create',
        'viagens_edit',
        'tickets_view',
        'profile_view',
        'profile_edit',
        'notifications_view',
        'notifications_manage',
        'notes_view',
        'notes_create',
        'notes_edit',
        'notes_delete'
    ])
).all()
collab_group.permissions_rel = collab_permissions

db.commit()
print("Permissões configuradas com sucesso!")
```

---

## 📡 API Reference

### Rotas de Gerenciamento de Permissões

#### Listar todas as permissões
```
GET /admin/permissions
```
Retorna página HTML com todas as permissões agrupadas por módulo.

#### Gerenciar permissões de grupos
```
GET /admin/permissions/groups
```
Retorna página HTML para configurar permissões de cada grupo.

#### Atualizar permissões de um grupo
```
POST /admin/permissions/groups/<group_id>/update
Body: permissions=[1,2,3,4,5]
```
Atualiza as permissões do grupo especificado.

#### API: Obter permissões de um grupo
```
GET /admin/api/permissions/groups/<group_id>
Response: {
    "group_id": 1,
    "group_name": "Administrador",
    "permission_ids": [1, 2, 3, 4, 5, ...]
}
```

#### API: Obter permissões por módulo
```
GET /admin/api/permissions/by-module
Response: {
    "viagens": [
        {"id": 1, "name": "Visualizar Viagens", "slug": "viagens_view", ...},
        {"id": 2, "name": "Criar Viagem", "slug": "viagens_create", ...}
    ],
    "tickets": [...]
}
```

---

## 🎓 Boas Práticas

### 1. Sempre usar decorators nas rotas
Nunca confie apenas na ocultação de elementos na interface. Sempre proteja as rotas com decorators.

### 2. Verificar permissões no controller
Se uma ação pode ser executada de múltiplas formas (botão, API, etc), verifique a permissão no controller também.

### 3. Permissões granulares
Prefira ter mais permissões específicas do que poucas permissões genéricas. Isso dá mais controle.

### 4. Documentar permissões necessárias
Ao criar novas funcionalidades, documente quais permissões são necessárias.

### 5. Testar diferentes perfis
Sempre teste suas funcionalidades com diferentes grupos de usuários para garantir que as permissões estão funcionando corretamente.

---

## 🐛 Troubleshooting

### Usuário não tem acesso mesmo tendo a permissão

1. Verifique se o usuário está no grupo correto:
```python
user = User.query.get(user_id)
print(user.groups)  # Lista os grupos
```

2. Verifique se o grupo tem a permissão:
```python
group = Group.query.get(group_id)
print([p.slug for p in group.permissions_rel])
```

3. Verifique se as permissões estão sendo carregadas:
```python
user = User.query.get(user_id)
print(user.get_all_permissions())
```

### Permissões não aparecem nos templates

Certifique-se de que o context processor está registrado no `routes.py`:
```python
app.context_processor(inject_user_permissions)
```

### Erro ao executar migrations

Se houver erro relacionado a chaves estrangeiras, execute na ordem:
1. Criar tabela `permissions`
2. Criar tabela `group_permissions`

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique esta documentação
2. Verifique os logs do sistema
3. Entre em contato com a equipe de desenvolvimento

---

**Última atualização**: 13/10/2024
**Versão**: 1.0.0
