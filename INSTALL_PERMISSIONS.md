# 🚀 Instalação do Sistema de Permissões

## Guia Rápido de Instalação

### Passo 1: Executar as Migrations

```bash
cd app-financeiro
python main.py --migrate
```

Isso criará as novas tabelas:
- `permissions` - Armazena todas as permissões do sistema
- `group_permissions` - Relaciona grupos com suas permissões

### Passo 2: Popular as Permissões

```bash
python database/seeders/permissions_seeder.py
```

Resultado esperado:
```
[SEEDER] Iniciando seed de permissões...
[SUCCESS] 67 permissões foram criadas com sucesso!

[INFO] Permissões criadas por módulo:
  - clientes: 5 permissões
  - configuracoes: 2 permissões
  - dashboard: 1 permissões
  - grupos: 4 permissões
  - integracoes: 6 permissões
  - licencas: 7 permissões
  - notificacoes: 2 permissões
  - notas: 4 permissões
  - perfil: 2 permissões
  - permissoes: 2 permissões
  - relatorios: 3 permissões
  - tickets: 6 permissões
  - usuarios: 5 permissões
  - viagens: 7 permissões
```

### Passo 3: Atribuir Permissões aos Grupos

```bash
python database/seeders/assign_group_permissions.py
```

Resultado esperado:
```
[SEEDER] Iniciando atribuição de permissões aos grupos...

[INFO] Configurando grupo: Administrador...
  ✓ 67 permissões atribuídas ao Administrador

[INFO] Configurando grupo: Gerente...
  ✓ 42 permissões atribuídas ao Gerente

[INFO] Configurando grupo: Colaborador...
  ✓ 15 permissões atribuídas ao Colaborador

[INFO] Configurando grupo: Financeiro...
  ✓ 35 permissões atribuídas ao Financeiro

[INFO] Configurando grupo: Suporte...
  ✓ 38 permissões atribuídas ao Suporte

[SUCCESS] Permissões atribuídas aos grupos com sucesso!

============================================================
RESUMO DAS PERMISSÕES POR GRUPO
============================================================
Administrador        |  67 permissões
Gerente              |  42 permissões
Financeiro           |  35 permissões
Suporte              |  38 permissões
Colaborador          |  15 permissões
============================================================
```

## ✅ Verificação

### 1. Verificar se as tabelas foram criadas

```bash
cd app-financeiro
python
```

```python
from app.models.database import SessionLocal
from app.models.permission import Permission
from app.models.group import Group

db = SessionLocal()

# Verificar permissões
permissions_count = db.query(Permission).count()
print(f"Total de permissões: {permissions_count}")
# Deve mostrar: Total de permissões: 67

# Verificar grupos com permissões
admin_group = db.query(Group).filter(Group.slug == 'admin').first()
print(f"Permissões do Admin: {len(admin_group.permissions_rel)}")
# Deve mostrar: Permissões do Admin: 67

db.close()
```

### 2. Testar no sistema

1. Acesse: `http://localhost:5000/admin/permissions`
2. Você verá a lista de todas as permissões organizadas por módulo

3. Acesse: `http://localhost:5000/admin/permissions/groups`
4. Você verá a interface para gerenciar permissões dos grupos

## 📋 Estrutura de Permissões por Grupo

### 👑 Administrador (67 permissões)
- **TODAS** as permissões do sistema
- Acesso total e irrestrito

### 👨‍💼 Gerente (42 permissões)
**Incluído:**
- ✅ Visualizar e gerenciar clientes
- ✅ Visualizar e gerenciar tickets
- ✅ Visualizar TODAS as viagens e aprovar
- ✅ Gerenciar integrações
- ✅ Visualizar e gerar licenças
- ✅ Visualizar usuários
- ✅ Gerar relatórios

**Não incluído:**
- ❌ Deletar clientes
- ❌ Criar/editar/deletar usuários
- ❌ Gerenciar permissões e grupos
- ❌ Editar configurações do sistema

### 👷 Colaborador (15 permissões)
**Incluído:**
- ✅ Visualizar dashboard
- ✅ Visualizar clientes
- ✅ Ver e criar tickets básicos
- ✅ Ver e criar suas próprias viagens
- ✅ Gerenciar notas pessoais
- ✅ Editar próprio perfil

**Não incluído:**
- ❌ Aprovar viagens
- ❌ Ver viagens de outros usuários
- ❌ Editar clientes
- ❌ Acessar integrações
- ❌ Gerenciar usuários

### 💰 Financeiro (35 permissões)
**Incluído:**
- ✅ Visualizar e editar clientes
- ✅ Visualizar tickets
- ✅ Visualizar TODAS as viagens e aprovar
- ✅ **Gerenciamento COMPLETO de licenças**
- ✅ Editar configurações
- ✅ Gerar relatórios

**Foco:**
- Gestão financeira
- Aprovação de despesas
- Licenciamento

### 🛠️ Suporte (38 permissões)
**Incluído:**
- ✅ Visualizar e editar clientes
- ✅ **Gerenciamento COMPLETO de tickets**
- ✅ **Gerenciamento COMPLETO de integrações**
- ✅ Gerenciar licenças e módulos
- ✅ Gerar relatórios

**Foco:**
- Atendimento ao cliente
- Gestão de tickets
- Manutenção de integrações

## 🔧 Personalização

### Adicionar nova permissão

1. Edite `database/seeders/permissions_seeder.py`
2. Adicione a nova permissão na lista `permissions_data`:

```python
{
    'name': 'Minha Nova Permissão',
    'slug': 'meu_modulo_acao',
    'description': 'Descrição da permissão',
    'module': 'meu_modulo'
},
```

3. Execute novamente o seeder:
```bash
python database/seeders/permissions_seeder.py
```

### Modificar permissões de um grupo

**Opção 1: Via interface administrativa**
1. Acesse: `http://localhost:5000/admin/permissions/groups`
2. Selecione o grupo
3. Marque/desmarque as permissões desejadas
4. Clique em "Salvar"

**Opção 2: Via script Python**
```python
from app.models.database import SessionLocal
from app.models.group import Group
from app.models.permission import Permission

db = SessionLocal()

# Buscar grupo
group = db.query(Group).filter(Group.slug == 'colaborador').first()

# Buscar permissões a adicionar
new_permissions = db.query(Permission).filter(
    Permission.slug.in_(['viagens_approve', 'tickets_edit'])
).all()

# Adicionar às permissões existentes
group.permissions_rel.extend(new_permissions)
db.commit()
```

## 🎯 Próximos Passos

### 1. Aplicar Decorators nas Rotas

Veja exemplos no arquivo `README_PERMISSIONS.md`, seção "Como Usar".

Exemplo básico:
```python
from app.utils.permissions_helper import permission_required

@permission_required('viagens_create')
def create_travel():
    return render_template('travels/create.html')
```

### 2. Controlar Elementos nos Templates

```html
{% if 'viagens_create' in user_permissions %}
<a href="{{ url_for('admin.travels_create') }}" class="btn btn-primary">
    Nova Viagem
</a>
{% endif %}
```

### 3. Criar Templates de Gerenciamento

Os templates básicos devem ser criados em:
- `templates/admin/permissions/list.html`
- `templates/admin/permissions/groups.html`

## 📚 Documentação Completa

Consulte `README_PERMISSIONS.md` para:
- Lista completa de todas as 67 permissões
- Exemplos detalhados de uso
- Boas práticas
- Troubleshooting
- API Reference

## ❗ Importante

1. **Sempre proteja as rotas**: Não confie apenas na ocultação de botões na interface
2. **Teste com diferentes perfis**: Certifique-se de testar com usuários de diferentes grupos
3. **Backup antes de modificar**: Sempre faça backup antes de modificar permissões em produção

## 🐛 Problemas Comuns

### "Permissões não aparecem nos templates"
**Solução**: Certifique-se de que o context processor está registrado no `routes.py`:
```python
app.context_processor(inject_user_permissions)
```

### "Usuário tem permissão mas não consegue acessar"
**Solução**: Verifique se:
1. O decorator está aplicado corretamente na rota
2. O usuário está no grupo correto
3. O grupo tem a permissão associada

### "Erro ao executar migrations"
**Solução**: Execute as migrations na ordem:
```bash
# 1. Limpar banco (CUIDADO: apaga dados)
python main.py --migrate-fresh

# 2. Popular permissões
python database/seeders/permissions_seeder.py

# 3. Atribuir aos grupos
python database/seeders/assign_group_permissions.py
```

## 📞 Suporte

Para dúvidas:
1. Consulte `README_PERMISSIONS.md`
2. Verifique os logs: `app-financeiro/logs/`
3. Entre em contato com a equipe de desenvolvimento

---

**Data de criação**: 13/10/2024
**Versão**: 1.0.0
