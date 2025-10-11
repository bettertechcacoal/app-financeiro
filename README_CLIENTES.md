# Sistema de Clientes - App Financeiro

## Resumo das Mudanças

Este documento descreve as implementações realizadas no sistema app-financeiro para gerenciamento de clientes vinculados a organizações do Movidesk.

## Mudanças Implementadas

### 1. Card "Vendas" renomeado para "Tickets"
- O card no dashboard principal foi renomeado de "Vendas" para "Tickets"
- O ícone foi alterado para `fa-ticket-alt` (ícone de ticket)
- A descrição foi atualizada para "Gerencie clientes e tickets de atendimento"
- Ao clicar no card, o usuário é redirecionado para a lista de clientes

### 2. Tela de Lista de Clientes
- **Rota:** `/admin/clients`
- **Template:** `templates/clients/list.html`
- Exibe todos os clientes cadastrados em uma tabela
- Mostra informações: ID, Nome, Email, Telefone, Organização, Documento
- Possui botões para editar e excluir clientes
- Exibe mensagem quando não há clientes cadastrados

### 3. Tela de Cadastro/Edição de Clientes
- **Rota Novo:** `/admin/clients/new`
- **Rota Editar:** `/admin/clients/<id>/edit`
- **Template:** `templates/clients/form.html`
- Formulário dividido em seções:
  - **Dados Pessoais:** Nome, CPF/CNPJ, Email, Telefone
  - **Organização:** Seleção de organização do Movidesk
  - **Endereço:** Endereço completo, Cidade, Estado, CEP

### 4. Integração com API de Organizações (tickets-api externo)
- O sistema se conecta a uma API externa (tickets-api) para buscar organizações do Movidesk
- **Nota:** O tickets-api NÃO faz parte deste projeto, é um serviço externo separado
- URL configurável via arquivo `.env` (variável `TICKETS_API_URL`)
- Botão "Carregar Organizações" no formulário de cadastro
- As organizações são carregadas dinamicamente via AJAX
- O cliente é vinculado à organização selecionada

### 5. Estrutura de Arquivos Criados

```
app-financeiro/
├── app/
│   ├── controllers/
│   │   └── clients/
│   │       └── clients_controller.py  (Controller de clientes)
│   └── services/
│       └── client_service.py          (Service para gerenciar clientes)
├── templates/
│   └── clients/
│       ├── list.html                  (Lista de clientes)
│       └── form.html                  (Formulário de cadastro/edição)
└── .env                               (Configuração da URL do tickets-api)
```

## Configuração

### Arquivo .env
Certifique-se de que o arquivo `.env` no `app-financeiro` contém:

```env
# Tickets API Configuration
TICKETS_API_URL=http://localhost:5001
```

### Porta do tickets-api (Externo)
O `tickets-api` é um serviço externo que deve estar rodando na **porta 5001** (configurável no `.env`).

## Como Usar

### 1. Instalar Dependências

```bash
cd app-financeiro
pip install -r requirements.txt
```

### 2. Iniciar o Servidor

**Terminal - app-financeiro (porta 5000):**
```bash
cd app-financeiro
python server.py
```

**Observação:** Certifique-se de que o serviço tickets-api externo esteja rodando e acessível na URL configurada no `.env`

### 2. Cadastrar um Cliente

1. Faça login no app-financeiro
2. No dashboard, clique no card "Tickets"
3. Clique em "Novo Cliente"
4. Preencha os dados pessoais (Nome, CPF/CNPJ, Email, Telefone)
5. Clique em "Carregar Organizações" para buscar as organizações do Movidesk
6. Selecione uma organização (opcional)
7. Preencha o endereço (opcional)
8. Clique em "Cadastrar Cliente"

### 3. Visualizar Clientes

- Acesse `/admin/clients` ou clique no card "Tickets" no dashboard
- Você verá a lista de todos os clientes cadastrados
- Cada cliente mostra a organização vinculada (se houver)

### 4. Editar/Excluir Cliente

- Na lista de clientes, use os botões de ação (editar/excluir)
- A edição permite alterar todos os dados, incluindo a organização
- A exclusão solicita confirmação antes de remover

## Rotas Disponíveis

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/admin/clients` | Lista todos os clientes |
| GET | `/admin/clients/new` | Formulário de novo cliente |
| POST | `/admin/clients/create` | Cria um novo cliente |
| GET | `/admin/clients/<id>/edit` | Formulário de edição |
| POST | `/admin/clients/<id>/update` | Atualiza um cliente |
| POST | `/admin/clients/<id>/delete` | Remove um cliente |
| GET | `/admin/api/organizations` | API para buscar organizações |

## Armazenamento de Dados

Atualmente, os clientes são armazenados **em memória** (no service). Para persistência, você pode:

1. Criar uma tabela no banco de dados
2. Implementar um modelo SQLAlchemy
3. Atualizar o `client_service.py` para usar o banco de dados

## Exemplo de Estrutura de Cliente

```python
{
    'id': 1,
    'name': 'João Silva',
    'email': 'joao@exemplo.com',
    'phone': '(11) 99999-9999',
    'document': '123.456.789-00',
    'organization_id': 'abc123',
    'organization_name': 'Empresa XYZ Ltda',
    'address': 'Rua Exemplo, 123',
    'city': 'São Paulo',
    'state': 'SP',
    'zipcode': '01234-567'
}
```

## Dependências Necessárias

Certifique-se de ter instalado:

```bash
pip install flask requests python-dotenv
```

## Próximos Passos Sugeridos

1. **Persistência de Dados:** Implementar banco de dados para armazenar clientes
2. **Validações:** Adicionar validações de CPF/CNPJ
3. **Busca/Filtros:** Implementar busca e filtros na lista de clientes
4. **Paginação:** Adicionar paginação para listas grandes
5. **Tickets:** Criar funcionalidade para gerenciar tickets vinculados aos clientes
6. **Integração Completa:** Sincronizar clientes com o Movidesk

## Observações Importantes

- O `tickets-api` precisa estar rodando para carregar as organizações
- As organizações vêm da API do Movidesk através do `tickets-api`
- O token do Movidesk deve estar configurado no `.env` do `tickets-api`
- Os clientes são armazenados em memória e serão perdidos ao reiniciar o servidor
