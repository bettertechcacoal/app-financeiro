# -*- coding: utf-8 -*-
"""
Script para corrigir o parâmetro MOVIDESK_SYNC_SCHEDULES
e movê-lo para o grupo de Integrações
"""
import sys
import os

# Adicionar o diretorio raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import SessionLocal
from app.models.parameter import Parameter
from app.models.parameter_group import ParameterGroup


def fix_movidesk_parameter():
    """Move o parâmetro MOVIDESK_SYNC_SCHEDULES para o grupo de Integrações"""

    db = SessionLocal()

    try:
        print("\n[FIX] Corrigindo parâmetro MOVIDESK_SYNC_SCHEDULES...")

        # Buscar o parâmetro
        parameter = db.query(Parameter).filter_by(parameter='MOVIDESK_SYNC_SCHEDULES').first()

        if not parameter:
            print("  [INFO] Parâmetro MOVIDESK_SYNC_SCHEDULES não encontrado. Nada a fazer.")
            return

        # Buscar o grupo de Integrações
        integrations_group = db.query(ParameterGroup).filter_by(name='Integrações').first()

        if not integrations_group:
            print("  [ERRO] Grupo 'Integrações' não encontrado!")
            return

        # Atualizar o parâmetro
        parameter.group_id = integrations_group.id
        parameter.description = 'Horários para sincronização automática de tickets do Movidesk'

        db.commit()

        print(f"  [OK] Parâmetro movido para o grupo 'Integrações' (ID: {integrations_group.id})")
        print(f"  [OK] Descrição atualizada")

        print(f"\n{'='*60}")
        print(f"Correção finalizada com sucesso!")
        print(f"{'='*60}\n")

    except Exception as e:
        db.rollback()
        print(f"\n[ERRO] Erro ao executar correção: {str(e)}\n")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("FIX: Parâmetro MOVIDESK_SYNC_SCHEDULES")
    print("="*60 + "\n")
    fix_movidesk_parameter()
