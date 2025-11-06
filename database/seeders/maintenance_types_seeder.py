# -*- coding: utf-8 -*-
"""
Seeder de Tipos de Manutenção
Popula a tabela de tipos de manutenção com categorias padrão para veículos
"""
import sys
from config import ROOT_DIR

sys.path.insert(0, ROOT_DIR)

from app.models.database import SessionLocal
from app.models.maintenance_type import MaintenanceType
from sqlalchemy import text


def seed_maintenance_types():
    """Cria tipos padrão de manutenção para gestão da frota"""
    db = SessionLocal()

    try:
        # Limpar tipos existentes
        db.execute(text("DELETE FROM maintenance_types"))

        # Lista de tipos de manutenção padrão
        maintenance_types_data = [
            {
                'name': 'Troca de Óleo',
                'description': 'Troca de óleo do motor e filtro de óleo'
            },
            {
                'name': 'Revisão Geral',
                'description': 'Revisão completa do veículo conforme manual do fabricante'
            },
            {
                'name': 'Troca de Filtros',
                'description': 'Troca de filtro de ar, combustível e cabine'
            },
            {
                'name': 'Alinhamento e Balanceamento',
                'description': 'Alinhamento de direção e balanceamento de rodas'
            },
            {
                'name': 'Troca de Pneus',
                'description': 'Substituição de pneus desgastados'
            },
            {
                'name': 'Freios',
                'description': 'Revisão e troca de pastilhas/lonas de freio'
            },
            {
                'name': 'Bateria',
                'description': 'Verificação e troca de bateria'
            },
            {
                'name': 'Suspensão',
                'description': 'Manutenção do sistema de suspensão'
            },
            {
                'name': 'Ar Condicionado',
                'description': 'Manutenção e recarga do sistema de ar condicionado'
            },
            {
                'name': 'Correia Dentada',
                'description': 'Troca da correia dentada e tensor'
            },
            {
                'name': 'Velas de Ignição',
                'description': 'Troca de velas de ignição'
            },
            {
                'name': 'Líquidos',
                'description': 'Verificação e troca de líquidos (freio, arrefecimento, direção)'
            },
            {
                'name': 'Sistema Elétrico',
                'description': 'Revisão do sistema elétrico e troca de lâmpadas'
            },
            {
                'name': 'Limpeza de Bicos',
                'description': 'Limpeza dos bicos injetores'
            },
            {
                'name': 'Geometria',
                'description': 'Ajuste de geometria da suspensão'
            },
        ]

        # Inserir tipos de manutenção
        for type_data in maintenance_types_data:
            maintenance_type = MaintenanceType(**type_data)
            db.add(maintenance_type)

        # Ajustar sequência de auto incremento do PostgreSQL
        db.execute(text("SELECT setval(pg_get_serial_sequence('maintenance_types', 'id'), (SELECT COALESCE(MAX(id), 1) FROM maintenance_types))"))
        db.commit()

        print("[SUCCESS] Seeder de tipos de manutenção executado com sucesso")

    except Exception as e:
        db.rollback()
        print(f"[ERRO] {type(e).__name__}: {str(e).split(chr(10))[0]}")
    finally:
        db.close()


if __name__ == '__main__':
    seed_maintenance_types()
