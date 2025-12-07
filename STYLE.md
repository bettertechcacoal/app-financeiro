# Guia de Estilo - App Financeiro

Este documento descreve todas as características do layout padrão utilizado nas páginas de listagem do sistema.

---

## Estrutura Base do Card

Todos os cards seguem uma estrutura de 3 partes: **Header**, **Body** e **Footer** (opcional).

```html
<div class="tw-card-section tw-card-shadow overflow-hidden hover:shadow-lg transition-shadow">
    <!-- Header -->
    <div class="px-5 py-3 bg-gradient-to-r from-gray-50 to-white border-b border-gray-100">
        ...
    </div>

    <!-- Body -->
    <div class="p-5">
        ...
    </div>

    <!-- Footer (opcional) -->
    <div class="px-5 py-3 border-t border-gray-100">
        ...
    </div>
</div>
```

### Classes Principais

| Classe | Descrição |
|--------|-----------|
| `tw-card-section` | Estilo base do card |
| `tw-card-shadow` | Sombra suave no card |
| `tw-input-field` | Estilo padrão para inputs |
| `tw-page-transition` | Animação de entrada da página |

---

## Header do Card

O header contém: ID, badges de status, e botões de ação.

```html
<div class="px-5 py-3 bg-gradient-to-r from-gray-50 to-white border-b border-gray-100">
    <div class="flex items-center justify-between">
        <!-- ID e Status -->
        <div class="flex items-center gap-3">
            <span class="font-medium text-[COR]-600">#{{ item.id }}</span>
            <!-- Badge de Status -->
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-[COR]-50 text-[COR]-700 border border-[COR]-200">
                <svg class="w-3.5 h-3.5">...</svg>
                Status
            </span>
        </div>

        <!-- Ações -->
        <div class="flex items-center gap-2">
            <!-- Dropdown Mobile -->
            <div class="relative lg:hidden">...</div>
            <!-- Botões Desktop -->
            <div class="hidden lg:flex gap-2">...</div>
        </div>
    </div>
</div>
```

---

## Badges de Status (Pill Style)

Os badges usam estilo "pill" com bordas arredondadas e cores suaves.

### Padrão de Cores

```html
<!-- Verde (Ativo/Sucesso) -->
<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
    <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
    </svg>
    Ativo
</span>

<!-- Vermelho (Inativo/Erro) -->
<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-red-50 text-red-700 border border-red-200">
    <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
    </svg>
    Inativo
</span>

<!-- Amarelo (Pendente/Alerta) -->
<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-amber-50 text-amber-700 border border-amber-200">
    <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
    </svg>
    Pendente
</span>

<!-- Cinza (Neutro) -->
<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700 border border-gray-200">
    <svg class="w-3.5 h-3.5">...</svg>
    Neutro
</span>
```

### Estrutura do Badge

- `rounded-full` - Bordas totalmente arredondadas (pill)
- `px-3 py-1` - Padding horizontal e vertical
- `text-xs font-medium` - Texto pequeno e semi-bold
- `bg-[COR]-50` - Background muito claro
- `text-[COR]-700` - Texto escuro
- `border border-[COR]-200` - Borda sutil
- `gap-1.5` - Espaço entre ícone e texto

---

## Botões de Ação

### Botões Desktop (Cores Suaves)

```html
<div class="hidden lg:flex gap-2 flex-shrink-0">
    <!-- Botão Editar -->
    <a href="..." class="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-cyan-700 bg-cyan-100 hover:bg-cyan-200 rounded-lg transition-colors">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
        </svg>
        Editar
    </a>

    <!-- Botão Ver -->
    <a href="..." class="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-emerald-700 bg-emerald-100 hover:bg-emerald-200 rounded-lg transition-colors">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
        </svg>
        Ver
    </a>

    <!-- Botão Excluir -->
    <button class="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-red-700 bg-red-100 hover:bg-red-200 rounded-lg transition-colors">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
        </svg>
        Excluir
    </button>
</div>
```

### Padrão de Cores para Botões

| Ação | Background | Texto | Hover |
|------|------------|-------|-------|
| Editar | `bg-cyan-100` | `text-cyan-700` | `hover:bg-cyan-200` |
| Ver | `bg-emerald-100` | `text-emerald-700` | `hover:bg-emerald-200` |
| Excluir | `bg-red-100` | `text-red-700` | `hover:bg-red-200` |
| Primário | `bg-blue-100` | `text-blue-700` | `hover:bg-blue-200` |
| Secundário | `bg-gray-100` | `text-gray-700` | `hover:bg-gray-200` |

---

## Dropdown Mobile (3 Pontos)

```html
<div class="relative lg:hidden">
    <button onclick="toggleDropdown({{ item.id }})" class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
        </svg>
    </button>
    <div id="dropdown-{{ item.id }}" class="hidden absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-2 z-10">
        <a href="..." class="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
            <svg class="w-4 h-4 text-cyan-500">...</svg>
            Editar
        </a>
        <a href="..." class="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
            <svg class="w-4 h-4 text-emerald-500">...</svg>
            Ver
        </a>
        <button class="w-full flex items-center gap-3 px-4 py-2 text-sm text-red-600 hover:bg-red-50">
            <svg class="w-4 h-4">...</svg>
            Excluir
        </button>
    </div>
</div>
```

### JavaScript do Dropdown

```javascript
function toggleDropdown(id) {
    // Fecha todos os outros dropdowns
    document.querySelectorAll('[id^="dropdown-"]').forEach(dropdown => {
        if (dropdown.id !== `dropdown-${id}`) {
            dropdown.classList.add('hidden');
        }
    });
    // Toggle do dropdown atual
    const dropdown = document.getElementById(`dropdown-${id}`);
    dropdown.classList.toggle('hidden');
}

// Fechar ao clicar fora
document.addEventListener('click', function(event) {
    if (!event.target.closest('[id^="dropdown-"]') && !event.target.closest('button')) {
        document.querySelectorAll('[id^="dropdown-"]').forEach(dropdown => {
            dropdown.classList.add('hidden');
        });
    }
});
```

---

## Body do Card

O body contém as informações principais em grid.

```html
<div class="p-5">
    <!-- Nome/Título Principal -->
    <div class="flex items-center gap-1.5 mb-4">
        <svg class="w-4 h-4 text-[COR]-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
        </svg>
        <p class="font-medium text-gray-900">{{ item.name }}</p>
    </div>

    <!-- Grid de Informações -->
    <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
        <div>
            <span class="text-xs font-medium text-gray-400 uppercase tracking-wide block mb-1">Label</span>
            <p class="font-medium text-gray-900 text-sm">Valor</p>
        </div>
        <div>
            <span class="text-xs font-medium text-gray-400 uppercase tracking-wide block mb-1">Outro Label</span>
            <p class="font-medium text-gray-900 text-sm">Outro Valor</p>
        </div>
    </div>
</div>
```

### Labels

- `text-xs` - Tamanho pequeno
- `font-medium` - Semi-bold
- `text-gray-400` - Cor cinza clara
- `uppercase` - Texto em maiúsculas
- `tracking-wide` - Espaçamento entre letras
- `block mb-1` - Bloco com margem inferior

---

## Barra de Pesquisa

```html
<div class="tw-card-section p-4 tw-card-shadow mb-6">
    <div class="flex items-center gap-4">
        <div class="flex-1 relative">
            <svg class="w-5 h-5 text-gray-400 absolute left-4 top-1/2 transform -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            <input type="text" id="searchInput" placeholder="Buscar..."
                   class="tw-input-field pl-12" onkeyup="filterItems()">
        </div>
        <button onclick="clearSearch()" class="btn btn-secondary">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
            Limpar
        </button>
    </div>
</div>
```

### JavaScript da Pesquisa

```javascript
function filterItems() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const rows = document.querySelectorAll('.item-row');
    let visibleCount = 0;

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });

    document.getElementById('visibleCount').textContent = visibleCount;
}

function clearSearch() {
    document.getElementById('searchInput').value = '';
    filterItems();
}
```

---

## Footer de Estatísticas

```html
<div class="tw-card-section tw-card-shadow mt-4 px-5 py-4">
    <div class="flex items-center justify-between">
        <div class="flex items-center gap-2 text-sm text-gray-500">
            <svg class="w-4 h-4 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
            Total: <span class="font-semibold text-gray-900" id="totalCount">{{ total }}</span>
        </div>
        <div class="flex items-center gap-2 text-sm text-gray-500">
            <svg class="w-4 h-4 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
            </svg>
            Mostrando: <span class="font-semibold text-gray-900" id="visibleCount">{{ visible }}</span>
        </div>
    </div>
</div>
```

---

## Botão Voltar

```html
<div class="mt-6">
    <a href="{{ url_for('admin.dashboard') }}" class="inline-flex items-center gap-2 text-teal-600 hover:text-teal-700 font-medium transition-colors">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
        </svg>
        Voltar para Dashboard
    </a>
</div>
```

---

## Estado Vazio (Empty State)

```html
<div class="col-span-full tw-card-section tw-card-shadow text-center py-16">
    <div class="w-20 h-20 bg-gray-100 rounded-3xl flex items-center justify-center mx-auto mb-6">
        <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
        </svg>
    </div>
    <h3 class="text-xl font-bold text-gray-900 mb-2">Nenhum item encontrado</h3>
    <p class="text-gray-500 mb-6">Descrição do estado vazio</p>
    <a href="..." class="btn btn-primary">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        Adicionar Novo
    </a>
</div>
```

---

## Ícones SVG Padrão

### Ícone de Usuário
```html
<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
</svg>
```

### Ícone de Email
```html
<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
</svg>
```

### Ícone de Telefone
```html
<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
</svg>
```

### Ícone de Documento
```html
<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
</svg>
```

### Ícone de Calendário
```html
<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
</svg>
```

### Ícone de Editar
```html
<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
</svg>
```

### Ícone de Excluir
```html
<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
</svg>
```

### Ícone de Olho (Ver)
```html
<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
</svg>
```

### Ícone de Check (Sucesso)
```html
<svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
</svg>
```

### Ícone de X (Erro/Fechar)
```html
<svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
</svg>
```

### Ícone de 3 Pontos (Menu)
```html
<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
</svg>
```

### Ícone de Seta Voltar
```html
<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
</svg>
```

### Ícone de Busca
```html
<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
</svg>
```

### Ícone de Plus (Adicionar)
```html
<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
</svg>
```

---

## Esquema de Cores por Página

| Página | Cor Principal | Uso |
|--------|---------------|-----|
| Tickets | `green/emerald` | IDs, badges, botões |
| Veículos | `cyan` | IDs, badges, botões |
| Licenças | `pink` | IDs, badges, botões |
| Usuários | `teal` | IDs, badges, botões |
| Viagens | `purple` | IDs, badges, botões |
| Notas | `yellow/orange` | IDs, badges, botões |

---

## Tipografia

| Elemento | Classes |
|----------|---------|
| Título Principal | `text-2xl font-bold text-gray-900` |
| Subtítulo | `text-gray-500` |
| Nome no Card | `font-medium text-gray-900` |
| Labels | `text-xs font-medium text-gray-400 uppercase tracking-wide` |
| Valores | `font-medium text-gray-900 text-sm` |
| IDs | `font-medium text-[COR]-600` |

---

## Espaçamento

| Elemento | Classes |
|----------|---------|
| Header do Card | `px-5 py-3` |
| Body do Card | `p-5` |
| Footer do Card | `px-5 py-3` |
| Gap entre Cards | `gap-4` ou `space-y-4` |
| Gap no Grid | `gap-4` |
| Margem Bottom | `mb-4`, `mb-6` |

---

## Responsividade

- `sm:` - Telas pequenas (640px+)
- `md:` - Telas médias (768px+)
- `lg:` - Telas grandes (1024px+)

### Padrões de Grid

```html
<!-- Grid padrão -->
<div class="grid grid-cols-2 sm:grid-cols-3 gap-4">

<!-- Grid de informações no body -->
<div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
```

### Visibilidade

```html
<!-- Apenas mobile -->
<div class="lg:hidden">

<!-- Apenas desktop -->
<div class="hidden lg:flex">
```

---

## Animações

- `transition-shadow` - Transição suave de sombra
- `transition-colors` - Transição suave de cores
- `hover:shadow-lg` - Sombra maior no hover
- `animate-fade-in` - Fade in na entrada (classe customizada)

---

## Modal de Confirmação de Exclusão

```html
<div id="deleteModal" class="fixed inset-0 bg-black bg-opacity-50 hidden items-center justify-center z-50">
    <div class="bg-white rounded-2xl p-6 w-full max-w-sm mx-4 shadow-2xl">
        <div class="text-center">
            <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>
            </div>
            <h3 class="text-lg font-bold text-gray-900 mb-2">Confirmar Exclusão</h3>
            <p class="text-gray-500 mb-6">Tem certeza que deseja excluir este item?</p>
            <div class="flex gap-3">
                <button onclick="closeDeleteModal()" class="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 font-medium">
                    Cancelar
                </button>
                <button onclick="confirmDelete()" class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium">
                    Excluir
                </button>
            </div>
        </div>
    </div>
</div>
```

---

## Checklist para Nova Página

- [ ] Usar `tw-card-section tw-card-shadow` nos cards
- [ ] Header com gradiente `bg-gradient-to-r from-gray-50 to-white`
- [ ] Badges em estilo pill com `rounded-full`
- [ ] Dropdown para mobile (`lg:hidden`)
- [ ] Botões desktop com cores suaves (`hidden lg:flex`)
- [ ] Labels em `uppercase tracking-wide`
- [ ] Barra de pesquisa com ícone SVG
- [ ] Footer de estatísticas
- [ ] Botão voltar
- [ ] Estado vazio estilizado
- [ ] Ícones SVG (não Font Awesome)
- [ ] Cores consistentes com o tema da página
