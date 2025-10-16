# -*- coding: utf-8 -*-
"""
Serviço de agendamento de tarefas automáticas
Gerencia a sincronização automática do Movidesk
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import json
import logging
from app.models.database import SessionLocal
from app.models.parameter import Parameter
from app.services.movidesk_service import MovideskService

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instância global do scheduler
scheduler = None


def init_scheduler(app):
    """Inicializa o scheduler de tarefas"""
    global scheduler

    if scheduler is not None:
        logger.warning("Scheduler já está inicializado")
        return scheduler

    scheduler = BackgroundScheduler(daemon=True)
    scheduler.start()

    logger.info("[SCHEDULER] Scheduler iniciado com sucesso")

    # Carregar e configurar horários de sincronização
    load_sync_schedules()

    # Atualizar horários a cada 5 minutos (caso sejam alterados via interface)
    scheduler.add_job(
        func=load_sync_schedules,
        trigger='interval',
        minutes=5,
        id='reload_schedules',
        name='Recarregar horários de sincronização',
        replace_existing=True
    )

    return scheduler


def load_sync_schedules():
    """Carrega os horários de sincronização do banco e configura jobs"""
    try:
        db = SessionLocal()

        # Buscar parâmetro com horários
        parameter = db.query(Parameter).filter_by(
            parameter='MOVIDESK_SYNC_SCHEDULES'
        ).first()

        if not parameter or not parameter.value:
            logger.info("[SCHEDULER] Nenhum horário de sincronização configurado")
            db.close()
            return

        # Parse JSON com horários
        schedules = json.loads(parameter.value)
        db.close()

        if not schedules or len(schedules) == 0:
            logger.info("[SCHEDULER] Lista de horários vazia")
            return

        # Remover jobs antigos de sincronização
        for job in scheduler.get_jobs():
            if job.id.startswith('sync_movidesk_'):
                scheduler.remove_job(job.id)

        # Adicionar novo job para cada horário
        for time_str in schedules:
            hour, minute = time_str.split(':')

            scheduler.add_job(
                func=sync_movidesk_tickets,
                trigger=CronTrigger(hour=int(hour), minute=int(minute)),
                id=f'sync_movidesk_{time_str.replace(":", "")}',
                name=f'Sincronização Movidesk às {time_str}',
                replace_existing=True
            )

            logger.info(f"[SCHEDULER] Job configurado para {time_str}")

        logger.info(f"[SCHEDULER] Total de {len(schedules)} horários configurados")

    except Exception as e:
        logger.error(f"[SCHEDULER] Erro ao carregar horários: {str(e)}")


def sync_movidesk_tickets():
    """
    Executa a sincronização automática de tickets do Movidesk
    Sincroniza os últimos 3 dias (dia atual + 2 dias anteriores)
    """
    try:
        logger.info("[SCHEDULER] Iniciando sincronização automática do Movidesk...")

        # Calcular datas (3 dias: hoje e mais 2 para trás)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=2)

        # Formatar datas para API
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        logger.info(f"[SCHEDULER] Período: {start_date_str} até {end_date_str}")

        # Executar sincronização
        movidesk_service = MovideskService()
        result = movidesk_service.sync_tickets(start_date_str, end_date_str)

        if result['success']:
            logger.info(
                f"[SCHEDULER] Sincronização concluída! "
                f"Novos: {result['synced']}, Atualizados: {result['updated']}, "
                f"Total: {result['total']}"
            )
        else:
            logger.error(f"[SCHEDULER] Erro na sincronização: {result.get('error')}")

    except Exception as e:
        logger.error(f"[SCHEDULER] Erro ao executar sincronização: {str(e)}")
        import traceback
        traceback.print_exc()


def shutdown_scheduler():
    """Desliga o scheduler gracefully"""
    global scheduler

    if scheduler is not None:
        scheduler.shutdown(wait=False)
        logger.info("[SCHEDULER] Scheduler desligado")


def get_scheduler():
    """Retorna a instância do scheduler"""
    return scheduler
