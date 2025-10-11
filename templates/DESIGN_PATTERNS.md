# Padrões de Projeto - Templates

## 📁 Estrutura de Pastas

A estrutura de templates foi reorganizada seguindo o padrão:

```
templates/
├── base.html                    # Template base
├── components/                  # Componentes reutilizáveis
│   ├── breadcrumbs.html
│   └── pagination.html
├── pages/                       # Páginas da aplicação
│   ├── auth/
│   │   └── login.html
│   ├── clients/
│   │   ├── form.html
│   │   └── manage.html
│   ├── tickets/
│   │   ├── list.html
│   │   └── view.html
│   ├── integrations/
│   │   ├── list.html
│   │   ├── movidesk_options.html
│   │   ├── movidesk_organizations.html
│   │   ├── movidesk_tickets.html
│   │   └── organization_edit.html
│   └── dashboard.html
└── reports/                     # Relatórios (futuro)
```

## 🎨 Padrões de Design

### 1. **Botões NUNCA dentro de Cards Centrais**

❌ **ERRADO:**
```html
<div class="card">
    <div class="text-center py-16">
        <h3>Nenhum registro encontrado</h3>
        <a href="/new" class="btn-primary">
            Cadastrar Novo
        </a>
    </div>
</div>
```

✅ **CORRETO:**
```html
<!-- Header com botão de ação -->
<div class="flex items-center justify-between mb-8">
    <div>
        <h1>Título da Página</h1>
        <p>Descrição</p>
    </div>
    <a href="/new" class="btn-primary">
        <i class="fas fa-plus mr-2"></i>
        Novo Registro
    </a>
</div>

<!-- Card sem botões -->
<div class="card">
    <div class="text-center py-16">
        <div class="w-20 h-20 bg-gray-100 rounded-3xl flex items-center justify-center mx-auto mb-6">
            <i class="fas fa-icon text-4xl text-gray-400"></i>
        </div>
        <h3>Nenhum registro encontrado</h3>
        <p>Clique no botão "Novo Registro" acima para começar</p>
    </div>
</div>
```

### 2. **Imports de Components**

Sempre use o prefixo `components/` para importar componentes:

```jinja2
{% from "components/breadcrumbs.html" import render as breadcrumbs %}
{% from "components/pagination.html" import render as pagination %}
```

### 3. **Render Template nos Controllers**

Sempre use o prefixo `pages/` nos controllers:

```python
# ✅ CORRETO
return render_template('pages/clients/manage.html', clients=clients)
return render_template('pages/auth/login.html')
return render_template('pages/dashboard.html')

# ❌ ERRADO
return render_template('clients/manage.html', clients=clients)
return render_template('login.html')
```

### 4. **Estrutura de Página Padrão**

```html
{% extends "base.html" %}
{% from "components/breadcrumbs.html" import render as breadcrumbs %}

{% block title %}Título da Página{% endblock %}

{% block breadcrumbs %}
{{ breadcrumbs([
    {'name': 'Seção', 'url': url_for('admin.section')},
    {'name': 'Página Atual'}
]) }}
{% endblock %}

{% block content %}
<div class="py-8">
    <!-- Header com ações -->
    <div class="mb-8 animate-fade-in">
        <div class="flex items-center justify-between">
            <div>
                <h1 class="text-3xl font-bold text-gray-900 mb-2">Título</h1>
                <p class="text-gray-600">Descrição</p>
            </div>
            <!-- Botões de ação aqui, FORA do card -->
            <a href="{{ url_for('admin.new') }}" class="btn-primary">
                <i class="fas fa-plus mr-2"></i>
                Nova Ação
            </a>
        </div>
    </div>

    <!-- Flash Messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="mb-6 p-4 rounded-xl {% if category == 'success' %}bg-green-100 text-green-700{% elif category == 'error' %}bg-red-100 text-red-700{% else %}bg-blue-100 text-blue-700{% endif %} animate-fade-in">
                    <i class="fas {% if category == 'success' %}fa-check-circle{% elif category == 'error' %}fa-exclamation-circle{% else %}fa-info-circle{% endif %} mr-2"></i>
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <!-- Conteúdo Principal (Card SEM botões) -->
    <div class="card animate-fade-in">
        <!-- Conteúdo aqui -->
    </div>
</div>
{% endblock %}
```

### 5. **Estados Vazios (Empty States)**

Quando não houver dados:

```html
<div class="text-center py-16">
    <div class="w-20 h-20 bg-gray-100 rounded-3xl flex items-center justify-center mx-auto mb-6">
        <i class="fas fa-icon text-4xl text-gray-400"></i>
    </div>
    <h3 class="text-xl font-bold text-gray-900 mb-2">Nenhum registro</h3>
    <p class="text-gray-600">Mensagem orientando o usuário a usar o botão acima</p>
</div>
```

## 📝 Regras Importantes

1. ✅ **Botões de ação** sempre no header da página, **NUNCA** dentro de cards
2. ✅ **Components** ficam na pasta `components/`
3. ✅ **Pages** ficam organizadas por módulo em `pages/`
4. ✅ **Reports** futuros ficam em `reports/`
5. ✅ Sempre usar `render_template('pages/...')` nos controllers
6. ✅ Sempre importar de `components/...` nos templates
7. ✅ Empty states devem orientar o usuário para o botão de ação no header

## 🔄 Migração Concluída

- ✅ Estrutura de pastas criada
- ✅ Macros renomeados para Components
- ✅ Arquivos reorganizados
- ✅ Controllers atualizados
- ✅ Referências atualizadas
- ✅ Botões removidos dos cards centrais
- ✅ Arquivos antigos removidos
