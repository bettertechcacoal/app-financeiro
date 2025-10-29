# -*- coding: utf-8 -*-
"""
Seeder para popular o banco de dados com parâmetros do sistema
"""
import sys
from config import ROOT_DIR

# Adicionar o diretorio raiz ao path
sys.path.insert(0, ROOT_DIR)

from app.models.database import SessionLocal
from app.models.parameter import Parameter, ParameterType
from app.models.parameter_group import ParameterGroup


def seed_parameters():
    """Popula o banco com parâmetros iniciais"""

    db = SessionLocal()

    try:
        print("\n[SEEDER] Criando parâmetros do sistema...")

        # Buscar grupos
        group_integracoes = db.query(ParameterGroup).filter_by(name='Integrações').first()
        group_email = db.query(ParameterGroup).filter_by(name='E-mail').first()
        group_sistema = db.query(ParameterGroup).filter_by(name='Sistema').first()
        group_viagens = db.query(ParameterGroup).filter_by(name='Viagens').first()

        # Parâmetros padrão do sistema
        parameters_data = [
            # Integrações
            {
                'parameter': 'MOVIDESK_TOKEN',
                'type': ParameterType.TEXT,
                'description': 'Token de autenticação no Movidesk',
                'value': '',
                'group_id': group_integracoes.id if group_integracoes else None
            },
            {
                'parameter': 'MOVIDESK_ENABLED',
                'type': ParameterType.CHECKBOX,
                'description': 'Habilitar integração com Movidesk',
                'value': 'N',
                'group_id': group_integracoes.id if group_integracoes else None
            },
            {
                'parameter': 'MOVIDESK_SYNC_SCHEDULES',
                'type': ParameterType.JSON,
                'description': 'Horários de sincronização automática do Movidesk',
                'value': '',
                'group_id': group_integracoes.id if group_integracoes else None
            },
            # E-mail
            {
                'parameter': 'SMTP_HOST',
                'type': ParameterType.TEXT,
                'description': 'Servidor SMTP para envio de e-mails',
                'value': 'smtp.gmail.com',
                'group_id': group_email.id if group_email else None
            },
            {
                'parameter': 'SMTP_PORT',
                'type': ParameterType.TEXT,
                'description': 'Porta do servidor SMTP',
                'value': '587',
                'group_id': group_email.id if group_email else None
            },
            {
                'parameter': 'SMTP_USER',
                'type': ParameterType.TEXT,
                'description': 'Usuário para autenticação SMTP',
                'value': '',
                'group_id': group_email.id if group_email else None
            },
            {
                'parameter': 'SMTP_PASSWORD',
                'type': ParameterType.TEXT,
                'description': 'Senha para autenticação SMTP',
                'value': '',
                'group_id': group_email.id if group_email else None
            },
            {
                'parameter': 'EMAIL_NOTIFICATIONS_ENABLED',
                'type': ParameterType.CHECKBOX,
                'description': 'Habilitar envio de notificações por e-mail',
                'value': 'S',
                'group_id': group_email.id if group_email else None
            },
            # Sistema
            {
                'parameter': 'SYSTEM_NAME',
                'type': ParameterType.TEXT,
                'description': 'Nome do sistema',
                'value': 'App Financeiro',
                'group_id': group_sistema.id if group_sistema else None
            },
            {
                'parameter': 'COMPANY_NAME',
                'type': ParameterType.TEXT,
                'description': 'Nome da empresa',
                'value': 'BetterTech',
                'group_id': group_sistema.id if group_sistema else None
            },
            {
                'parameter': 'DEFAULT_LANGUAGE',
                'type': ParameterType.SELECT,
                'description': 'Idioma padrão do sistema',
                'value': 'pt-BR',
                'options': '["pt-BR", "en-US", "es-ES"]',
                'group_id': group_sistema.id if group_sistema else None
            },
            # Viagens
            {
                'parameter': 'AUTO_APPROVE_TRAVELS',
                'type': ParameterType.CHECKBOX,
                'description': 'Aprovar viagens automaticamente',
                'value': 'N',
                'group_id': group_viagens.id if group_viagens else None
            },
            {
                'parameter': 'MAX_TRAVEL_DAYS',
                'type': ParameterType.TEXT,
                'description': 'Número máximo de dias para uma viagem',
                'value': '30',
                'group_id': group_viagens.id if group_viagens else None
            },
            {
                'parameter': 'MEAL_PRICES',
                'type': ParameterType.JSON,
                'description': 'Valores padrão das refeições',
                'value': '{"breakfast":"15.00","lunch":"25.00","dinner":"25.00"}',
                'group_id': group_viagens.id if group_viagens else None
            }
        ]

        created_count = 0
        updated_count = 0

        for param_data in parameters_data:
            # Verifica se o parâmetro já existe
            existing_param = db.query(Parameter).filter_by(
                parameter=param_data['parameter']
            ).first()

            if not existing_param:
                # Criar novo parâmetro
                param = Parameter(**param_data)
                db.add(param)
                created_count += 1
                print(f"  [OK] Parâmetro criado: {param_data['parameter']}")
            else:
                # Atualizar apenas a descrição e grupo (mantém o valor existente)
                existing_param.description = param_data['description']
                existing_param.type = param_data['type']
                existing_param.group_id = param_data.get('group_id')
                if 'options' in param_data:
                    existing_param.options = param_data['options']
                updated_count += 1
                print(f"  [OK] Parâmetro atualizado: {param_data['parameter']}")

        db.commit()

        print(f"\n{'='*60}")
        print(f"Seeder finalizado com sucesso!")
        print(f"Parâmetros criados: {created_count}")
        print(f"Parâmetros atualizados: {updated_count}")
        print(f"Total de parâmetros: {len(parameters_data)}")
        print(f"{'='*60}\n")

    except Exception as e:
        db.rollback()
        print(f"\n[ERRO] Erro ao executar seeder: {str(e)}\n")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("SEEDER: Parâmetros do Sistema")
    print("="*60 + "\n")
    seed_parameters()
