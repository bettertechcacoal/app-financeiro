# 📐 Guia de Estilo e Padronização - Sistema Financeiro

> Documento de referência para manter a consistência visual e de código em todas as telas do sistema.

---

## 🎨 Paleta de Cores

### Cores Principais
```css
Azul Principal:    from-blue-500 to-blue-600   /* Gradientes de ícones */
Verde Sucesso:     bg-green-500, bg-green-600  /* Botões de ação positiva */
Vermelho Alerta:   bg-red-500, bg-red-600      /* Labels obrigatórios, alertas */
Cinza Neutro:      bg-gray-50, bg-gray-100     /* Backgrounds, borders */
```

### Cores de Texto
```css
Título Principal:  text-gray-900               /* Títulos H1 */
Subtítulo:         text-gray-600               /* Descrições, subtítulos */
Texto Corpo:       text-gray-700               /* Texto normal */
Texto Secundário:  text-gray-500               /* Placeholders, hints */
Labels:            text-gray-700               /* Labels normais */
Labels Obrigatórios: text-red-600             /* Labels com * */
```

### Cores de Estado
```css
Ativo:             bg-green-500 text-white
Inativo:           bg-white text-green-500 (com border)
Hover:             hover:bg-green-600, hover:shadow-lg
Focus:             focus:ring-2 focus:ring-blue-500
```

---

## 📏 Tipografia

### Tamanhos de Fonte
```css
/* Headers de Página */
H1 (Título Principal):     text-2xl sm:text-3xl font-bold
H2 (Subtítulo):            text-sm sm:text-base
H3 (Seção):                text-lg font-bold

/* Formulários */
Labels:                    text-xs font-bold uppercase
Inputs:                    text-base (14-16px)
Placeholders:              text-gray-400

/* Botões */
Botão Principal:           text-sm sm:text-base font-semibold
Botão Secundário:          text-sm font-semibold

/* Tabs */
Tab Item:                  text-sm sm:text-base font-semibold
```

### Peso da Fonte
```css
Normal:            font-normal (400)
Médio:             font-medium (500)
Semibold:          font-semibold (600)
Bold:              font-bold (700)
```

---

## 📦 Componentes

### 🎯 Header de Página

```html
<!-- Header Padrão com Botões de Ação -->
<div class="mb-8 animate-fade-in">
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-4">
        <div class="flex items-center">
            <!-- Ícone -->
            <div class="w-14 h-14 sm:w-16 sm:h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center shadow-lg mr-4 flex-shrink-0">
                <i class="fas fa-icon-name text-white text-2xl sm:text-3xl"></i>
            </div>

            <!-- Título -->
            <div>
                <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-1">
                    Título da Página
                </h1>
                <p class="text-sm sm:text-base text-gray-600">
                    Descrição ou subtítulo
                </p>
            </div>
        </div>

        <!-- Botões de Ação (Padrão) -->
        <div class="flex flex-wrap gap-3">
            <!-- Botão Voltar (Opcional) -->
            <a href="{{ url_for('route.list') }}"
               class="inline-flex items-center px-6 py-2 border border-gray-300 rounded-lg text-gray-700 font-semibold hover:bg-gray-50 transition-all">
                <i class="fas fa-arrow-left mr-2"></i>
                Voltar
            </a>

            <!-- Botão Pesquisar (Quando necessário) -->
            <button type="button"
                    class="inline-flex items-center px-6 py-2 border border-gray-300 rounded-lg text-gray-700 font-semibold hover:bg-gray-50 transition-all">
                <i class="fas fa-search mr-2"></i>
                Pesquisar
            </button>

            <!-- Botão Salvar (Primário) -->
            <!-- IMPORTANTE: Sempre usar "Salvar" independente se é criar ou atualizar -->
            <button type="submit" form="form-id"
                    class="inline-flex items-center px-8 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-all shadow-md hover:shadow-lg">
                <i class="fas fa-save mr-2"></i>
                Salvar
            </button>
        </div>
    </div>
</div>
```

**Especificações:**
- Ícone: `w-14 h-14 sm:w-16 sm:h-16`
- Gradiente: `from-blue-500 to-blue-600` (pode variar por contexto)
- Título: `text-2xl sm:text-3xl font-bold text-gray-900`
- Subtítulo: `text-sm sm:text-base text-gray-600`
- **Botões no Header**: sempre à direita, com `gap-3`
- **Ordem**: Voltar → Pesquisar → Salvar (da esquerda para direita)

---

### 📝 Inputs e Formulários

#### Input Padrão
```html
<div class="mb-6">
    <label class="block text-xs font-bold text-gray-700 uppercase mb-2">
        Nome do Campo
    </label>
    <input
        type="text"
        name="field_name"
        placeholder="Digite aqui..."
        class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
    >
</div>
```

#### Input Obrigatório
```html
<div class="mb-6">
    <label class="block text-xs font-bold text-red-600 uppercase mb-2">
        Nome do Campo *
    </label>
    <input
        type="text"
        name="field_name"
        placeholder="Digite aqui..."
        required
        class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
    >
</div>
```

#### Select/Dropdown
```html
<div class="mb-6">
    <label class="block text-xs font-bold text-gray-700 uppercase mb-2">
        Selecione
    </label>
    <select
        name="field_name"
        class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
    >
        <option value="">Selecione uma opção</option>
        <option value="1">Opção 1</option>
    </select>
</div>
```

#### Textarea
```html
<div class="mb-6">
    <label class="block text-xs font-bold text-gray-700 uppercase mb-2">
        Descrição
    </label>
    <textarea
        name="field_name"
        rows="4"
        placeholder="Digite aqui..."
        class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
    ></textarea>
</div>
```

**Especificações:**
- Padding: `px-4 py-3`
- Border: `border border-gray-300`
- Arredondamento: `rounded-xl`
- Focus: `focus:ring-2 focus:ring-blue-500 focus:border-blue-500`
- Transição: `transition-all`

---

### 🔘 Botões

#### Botão Primário (Salvar)
**IMPORTANTE:** Sempre usar "Salvar" independente se é criação ou atualização
```html
<button
    type="submit"
    class="w-full sm:w-auto px-8 py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition-all shadow-lg hover:shadow-xl"
>
    <i class="fas fa-save mr-2"></i>
    Salvar
</button>
```

#### Botão Secundário (Cancelar)
```html
<a
    href="{{ url_for('route_name') }}"
    class="w-full sm:w-auto px-6 py-3 border border-gray-300 rounded-xl text-gray-700 font-semibold hover:bg-gray-50 transition-all text-center"
>
    <i class="fas fa-times mr-2"></i>
    Cancelar
</a>
```

#### Botão de Sucesso (Adicionar/Criar)
```html
<button
    type="button"
    class="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-xl font-semibold hover:bg-green-700 transition-all shadow-md hover:shadow-lg"
>
    <i class="fas fa-plus mr-2"></i>
    Adicionar
</button>
```

#### Botão Voltar (Link)
```html
<div class="mt-6 animate-fade-in">
    <a href="{{ url_for('route_name') }}" class="text-blue-600 hover:text-blue-700 font-semibold">
        <i class="fas fa-arrow-left mr-2"></i>
        Voltar para Lista
    </a>
</div>
```

**Especificações:**
- Primário: `bg-blue-600 hover:bg-blue-700`
- Secundário: `border border-gray-300 hover:bg-gray-50`
- Sucesso: `bg-green-600 hover:bg-green-700`
- Padding: `px-6 py-3` ou `px-8 py-3`
- Arredondamento: `rounded-xl`
- Sombra: `shadow-lg hover:shadow-xl`

---

### 📑 Tabs

```html
<!-- Navegação de Tabs -->
<div class="flex gap-6 md:gap-8 border-b-2 border-gray-200 px-4 md:px-6 overflow-x-auto scrollbar-thin scrollbar-thumb-gray-300">
    <div class="tab-item py-3 font-semibold text-gray-900 border-b-3 border-blue-600 cursor-pointer transition-all whitespace-nowrap flex-shrink-0 active" data-tab="tab1">
        Tab 1
    </div>
    <div class="tab-item py-3 font-semibold text-gray-500 border-b-3 border-transparent hover:text-gray-700 cursor-pointer transition-all whitespace-nowrap flex-shrink-0" data-tab="tab2">
        Tab 2
    </div>
</div>

<!-- Conteúdo das Tabs -->
<div class="p-4 md:p-6 lg:p-8">
    <div class="tab-content active" id="tab-tab1">
        <!-- Conteúdo Tab 1 -->
    </div>
    <div class="tab-content" id="tab-tab2">
        <!-- Conteúdo Tab 2 -->
    </div>
</div>
```

**CSS Necessário:**
```css
.tab-content {
    display: none;
}
.tab-content.active {
    display: block;
}
```

**JavaScript (jQuery):**
```javascript
$('.tab-item').on('click', function() {
    const tabName = $(this).data('tab');

    // Remove active state
    $('.tab-item').each(function() {
        $(this).removeClass('text-gray-900 border-blue-600').addClass('text-gray-500 border-transparent');
    });

    $('.tab-content').removeClass('active');

    // Add active state
    $(this).removeClass('text-gray-500 border-transparent').addClass('text-gray-900 border-blue-600');
    $('#tab-' + tabName).addClass('active');
});
```

---

### 📋 Cards

#### Card Padrão
```html
<div class="card animate-fade-in">
    <div class="p-4 md:p-6 lg:p-8">
        <!-- Conteúdo -->
    </div>
</div>
```

#### Card com Header
```html
<div class="card animate-fade-in">
    <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-bold text-gray-800">Título do Card</h3>
    </div>
    <div class="p-4 md:p-6 lg:p-8">
        <!-- Conteúdo -->
    </div>
</div>
```

---

### 🔄 Toggle de Status (Ativo/Inativo)

```html
<div class="inline-flex border border-green-500 rounded-lg overflow-hidden">
    <button
        type="button"
        class="status-btn px-6 py-2 bg-green-500 text-white font-semibold text-sm transition-all hover:bg-green-600"
    >
        ATIVO
    </button>
    <button
        type="button"
        class="status-btn px-6 py-2 bg-white text-green-500 font-semibold text-sm transition-all hover:bg-gray-50"
    >
        INATIVO
    </button>
</div>
```

**JavaScript (jQuery):**
```javascript
$('.status-btn').on('click', function() {
    $('.status-btn').each(function() {
        $(this).removeClass('bg-green-500 text-white').addClass('bg-white text-green-500');
    });
    $(this).removeClass('bg-white text-green-500').addClass('bg-green-500 text-white');
});
```

---

## 🎯 Layout e Grid

### Grid Responsivo (Formulários)
```html
<!-- 1 coluna em mobile, 2 em tablet, 3 em desktop -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
    <div>Campo 1</div>
    <div>Campo 2</div>
    <div>Campo 3</div>
</div>

<!-- Campo que ocupa 2 colunas -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6">
    <div class="md:col-span-2">Campo Grande</div>
    <div>Campo Pequeno</div>
</div>

<!-- Apenas 2 colunas -->
<div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
    <div>Campo 1</div>
    <div>Campo 2</div>
</div>
```

### Espaçamento
```css
Gap entre elementos:       gap-4 md:gap-6
Margem bottom:             mb-4, mb-6, mb-8
Padding interno:           p-4 md:p-6 lg:p-8
Padding lateral:           px-4 md:px-6
Padding vertical:          py-4 md:py-6
```

---

## 📍 Posicionamento Padrão

### Botões de Ação Principais

**IMPORTANTE:** Os botões de ação principais (Voltar, Pesquisar, Salvar) devem ficar **no header da página**, não no final do formulário!

```html
<!-- Botões no Header (Padrão Correto) -->
<div class="mb-8 animate-fade-in">
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-4">
        <div class="flex items-center">
            <!-- Ícone e Título aqui -->
        </div>

        <!-- Botões de Ação -->
        <div class="flex flex-wrap gap-3">
            <a href="{{ url_for('route.list') }}"
               class="inline-flex items-center px-6 py-2 border border-gray-300 rounded-lg text-gray-700 font-semibold hover:bg-gray-50 transition-all">
                <i class="fas fa-arrow-left mr-2"></i>
                Voltar
            </a>
            <button type="submit" form="form-id"
                    class="inline-flex items-center px-8 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-all shadow-md hover:shadow-lg">
                <i class="fas fa-save mr-2"></i>
                Salvar
            </button>
        </div>
    </div>
</div>
```

**Especificações:**
- **Localização**: No header da página, à direita
- **Container**: `flex flex-wrap gap-3`
- **Ordem padrão**: Voltar → Pesquisar (se necessário) → Salvar
- **Botão Voltar**: `border border-gray-300` (secundário)
- **Botão Salvar**: `bg-blue-600` (primário)
- **Form Submit**: usar `form="form-id"` para submit de formulário externo

**Quando usar cada botão:**
- **Voltar**: Em todas as telas de cadastro/edição
- **Pesquisar**: Apenas em telas de listagem/busca
- **Salvar**: Em telas de formulário (cadastro/edição)
  - **IMPORTANTE**: Sempre usar texto "Salvar", nunca "Atualizar" ou "Confirmar"
  - Nomenclatura padrão independente da operação (criar ou atualizar)

### ❌ NÃO FAZER

```html
<!-- ❌ ERRADO: Botões no final do formulário -->
<div class="flex justify-end gap-4 pt-8 mt-8 border-t">
    <button>Cancelar</button>
    <button>Salvar</button>
</div>

<!-- ❌ ERRADO: Botão Voltar separado após o card -->
<div class="mt-6">
    <a href="#">Voltar para Lista</a>
</div>
```

**Por quê?**
- Botões no header são mais acessíveis
- Usuário não precisa rolar a página para salvar
- Padrão consistente em todas as telas
- Melhor UX em dispositivos móveis

---

## 🎨 Estados Vazios (Empty States)

### ✅ Padrão Correto (Sem botões de navegação)

```html
<!-- Estado vazio SIMPLES - apenas informação -->
<div class="text-center py-16">
    <div class="w-20 h-20 bg-gray-100 rounded-3xl flex items-center justify-center mx-auto mb-6">
        <i class="fas fa-icon-name text-4xl text-gray-400"></i>
    </div>
    <h3 class="text-xl font-bold text-gray-900 mb-2">Nenhum item encontrado</h3>
    <p class="text-gray-600">Mensagem explicativa sobre como adicionar itens</p>
</div>
```

### ❌ NÃO FAZER - Botões de navegação em estados vazios

**IMPORTANTE:** Nunca adicione botões de navegação como "Ir para...", "Acessar...", etc. no centro do conteúdo ou em estados vazios!

```html
<!-- ❌ ERRADO: Botão de navegação no empty state -->
<div class="text-center py-16">
    <h3 class="text-xl font-bold text-gray-900 mb-2">Nenhuma organização cadastrada</h3>
    <p class="text-gray-600 mb-6">Cadastre organizações primeiro para visualizar tickets</p>
    <a href="{{ url_for('admin.clients_list') }}" class="btn-primary">
        <i class="fas fa-users mr-2"></i>
        Ir para Clientes  <!-- ❌ NUNCA FAZER ISSO -->
    </a>
</div>
```

**Por quê?**
- Botões no meio do conteúdo quebram o fluxo visual
- Cria inconsistência na navegação
- Usuários devem usar breadcrumbs ou menu lateral para navegar
- Estados vazios devem apenas informar, não forçar navegação

**O que fazer em vez disso:**
- Use apenas mensagens informativas
- Deixe a navegação para o menu/breadcrumbs
- Se realmente necessário, use links de texto discretos (não botões)

### ✅ Alternativa Aceitável (Link discreto)

```html
<div class="text-center py-16">
    <div class="w-20 h-20 bg-gray-100 rounded-3xl flex items-center justify-center mx-auto mb-6">
        <i class="fas fa-icon-name text-4xl text-gray-400"></i>
    </div>
    <h3 class="text-xl font-bold text-gray-900 mb-2">Nenhum item encontrado</h3>
    <p class="text-gray-600">
        Mensagem explicativa.
        <a href="{{ url_for('route') }}" class="text-blue-600 hover:text-blue-700 underline">
            Clique aqui para mais informações
        </a>
    </p>
</div>
```

---

## 📱 Responsividade

### Breakpoints Tailwind
```css
sm:  640px   /* Tablets pequenos */
md:  768px   /* Tablets */
lg:  1024px  /* Desktops */
xl:  1280px  /* Desktops grandes */
2xl: 1536px  /* Telas muito grandes */
```

### Padrões Responsivos
```html
<!-- Texto responsivo -->
<h1 class="text-2xl sm:text-3xl lg:text-4xl">Título</h1>

<!-- Ícone responsivo -->
<div class="w-14 h-14 sm:w-16 sm:h-16">Ícone</div>

<!-- Grid responsivo -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">

<!-- Flex responsivo -->
<div class="flex flex-col sm:flex-row">

<!-- Padding responsivo -->
<div class="p-4 md:p-6 lg:p-8">

<!-- Gap responsivo -->
<div class="gap-4 md:gap-6 lg:gap-8">
```

---

## ⚡ Animações

### Classes de Animação
```css
animate-fade-in      /* Fade in suave */
transition-all       /* Transição suave em todos os elementos */
hover:shadow-lg      /* Sombra no hover */
hover:shadow-xl      /* Sombra maior no hover */
```

### Uso Recomendado
```html
<!-- Cards -->
<div class="card animate-fade-in">

<!-- Botões -->
<button class="transition-all hover:shadow-lg">

<!-- Links -->
<a class="transition-all hover:text-blue-700">
```

---

## 🔍 Ícones (Font Awesome)

### Padrões de Uso
```html
<!-- Ícones de Header -->
<i class="fas fa-user-tie text-white text-2xl sm:text-3xl"></i>

<!-- Ícones em Títulos de Seção -->
<i class="fas fa-user-circle text-blue-600 mr-2"></i>

<!-- Ícones em Botões -->
<i class="fas fa-save mr-2"></i>
<i class="fas fa-times mr-2"></i>
<i class="fas fa-plus mr-2"></i>
<i class="fas fa-arrow-left mr-2"></i>

<!-- Ícones Empty State -->
<i class="fas fa-icon-name text-gray-400 text-4xl"></i>
```

### Ícones Comuns
- `fa-user-tie` - Pessoa/Cliente
- `fa-building` - Organização
- `fa-ticket-alt` - Tickets
- `fa-users` - Contatos
- `fa-map-marker-alt` - Endereços
- `fa-credit-card` - Cobrança
- `fa-th-large` - Módulos
- `fa-save` - Salvar
- `fa-times` - Cancelar/Fechar
- `fa-plus` - Adicionar
- `fa-arrow-left` - Voltar

---

## 📋 Mensagens Flash

```html
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
```

---

## ✅ Checklist de Implementação

Ao criar uma nova tela, certifique-se de:

- [ ] Usar header padrão com ícone gradiente
- [ ] Labels obrigatórios em vermelho (`text-red-600`)
- [ ] Inputs com `rounded-xl` e `focus:ring-2 focus:ring-blue-500`
- [ ] Botões de ação posicionados no final (`justify-end`)
- [ ] Botão Voltar após o card (`mt-6`)
- [ ] Grid responsivo (`grid-cols-1 md:grid-cols-2`)
- [ ] Padding responsivo (`p-4 md:p-6 lg:p-8`)
- [ ] Animações (`animate-fade-in`, `transition-all`)
- [ ] Classes Tailwind puras (evitar CSS customizado)
- [ ] Ícones Font Awesome apropriados
- [ ] Empty states para seções vazias
- [ ] Mensagens flash padronizadas

---

## 📚 Exemplos de Referência

Telas de referência no projeto:
- `templates/clients/form.html` - Formulário completo com tabs
- `templates/tickets/list.html` - Listagem com tabela
- `templates/integrations/list.html` - Grid de cards
- `templates/dashboard.html` - Layout de dashboard

---

**Última atualização:** Outubro 2025
**Versão:** 1.0
**Tecnologias:** Tailwind CSS 3.x, Font Awesome 6.x, jQuery 3.7.x
