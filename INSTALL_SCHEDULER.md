# Instalação do Sistema de Sincronização Automática

## 1. Instalar Dependências

Execute o comando abaixo para instalar as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

Ou instale manualmente:

```bash
pip install apscheduler==3.10.4
```

## 2. Verificar Configuração

O sistema de sincronização automática foi integrado ao `main.py` e será inicializado automaticamente quando o servidor Flask for iniciado.

## 3. Configurar Horários de Sincronização

1. Acesse: `/admin/integrations/movidesk/tickets`
2. Na seção "Sincronização Automática"
3. Adicione os horários desejados (ex: 08:00, 12:00, 18:00)
4. Os horários são salvos automaticamente

## 4. Como Funciona

### Sincronização Manual
- Usuário clica em "Sincronizar Agora"
- Define período de até 5 dias
- Executa sincronização imediatamente

### Sincronização Automática
- **Frequência**: Executa nos horários configurados
- **Período**: Sempre os últimos 3 dias (hoje + 2 dias anteriores)
- **Exemplo**: Se hoje é dia 16, sincroniza dias 14, 15 e 16
- **Background**: Roda em thread separada, não trava o sistema
- **Logs**: Registra todas as execuções no console

### Atualização de Horários
- O scheduler verifica novos horários a cada 5 minutos
- Alterações na interface são aplicadas automaticamente
- Não é necessário reiniciar o servidor

## 5. Logs e Monitoramento

Os logs aparecem no console do servidor:

```
[SCHEDULER] Scheduler iniciado com sucesso
[SCHEDULER] Job configurado para 08:00
[SCHEDULER] Job configurado para 12:00
[SCHEDULER] Total de 2 horários configurados
[SCHEDULER] Iniciando sincronização automática do Movidesk...
[SCHEDULER] Período: 2025-10-14 até 2025-10-16
[SCHEDULER] Sincronização concluída! Novos: 45, Atualizados: 12, Total: 57
```

## 6. Troubleshooting

### Scheduler não inicia
- Verifique se o APScheduler está instalado: `pip show apscheduler`
- Confira os logs ao iniciar o servidor

### Jobs não executam
- Verifique se há horários configurados no parâmetro `MOVIDESK_SYNC_SCHEDULES`
- Confira se o formato dos horários está correto (HH:MM)
- Verifique os logs do scheduler

### Sincronização falha
- Verifique a variável de ambiente `MOVIDESK_TOKEN`
- Confirme conexão com a API do Movidesk
- Consulte os logs de erro no console

## 7. Parâmetro no Banco

O parâmetro `MOVIDESK_SYNC_SCHEDULES` é armazenado na tabela `parameters`:

- **Nome**: `MOVIDESK_SYNC_SCHEDULES`
- **Tipo**: `TEXT`
- **Grupo**: `Integrações`
- **Formato**: JSON array de strings
- **Exemplo**: `["08:00", "12:00", "15:00", "18:00"]`

## 8. Corrigir Parâmetro Existente

Se o parâmetro foi criado antes da atualização e está fora do grupo:

```bash
cd C:\Python\bettertech\app-financeiro
python database/seeders/fix_movidesk_parameter.py
```

## 9. Parar o Scheduler

O scheduler é desligado automaticamente ao parar o servidor Flask (Ctrl+C).
