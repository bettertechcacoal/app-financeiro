# -*- coding: utf-8 -*-
from app.models.database import SessionLocal
from app.models.license import License
from datetime import datetime, date
from sqlalchemy import func
import requests
import urllib.parse


class LicenseService:
    """Serviço para gerenciamento de licenças"""

    def process_and_save_file(self, file_content):
        """Processa arquivo TXT e salva no banco (com sobrescrita)"""
        db = SessionLocal()
        try:
            saved_count = 0
            dates_processed = set()

            for line in file_content.strip().split('\n'):
                if not line.strip():
                    continue

                parts = line.split(',')
                if len(parts) >= 5:
                    client_code = parts[0].strip()
                    module_code = parts[1].strip()
                    license_date = datetime.strptime(parts[2].strip(), '%d/%m/%Y').date()
                    password = parts[3].strip()
                    client_name = parts[4].strip()

                    # Rastrear datas processadas
                    dates_processed.add((client_code, license_date))

                    # Verificar se já existe
                    existing = db.query(License).filter(
                        License.client_code == client_code,
                        License.module_code == module_code,
                        License.license_date == license_date
                    ).first()

                    if existing:
                        # Atualizar (sobrescrever)
                        existing.password = password
                        existing.client_name = client_name
                    else:
                        # Criar novo
                        license_obj = License(
                            client_code=client_code,
                            client_name=client_name,
                            license_date=license_date,
                            module_code=module_code,
                            password=password
                        )
                        db.add(license_obj)

                    saved_count += 1

            db.commit()
            return saved_count, len(dates_processed)
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def get_unique_clients(self):
        """Retorna lista de clientes únicos do banco de licenças com contagem de datas"""
        db = SessionLocal()
        try:
            # Buscar clientes únicos com contagem de datas distintas, ordenados por nome
            results = db.query(
                License.client_code,
                License.client_name,
                func.count(func.distinct(License.license_date)).label('dates_count')
            ).group_by(
                License.client_code,
                License.client_name
            ).order_by(License.client_name.asc()).all()

            return [{'code': r[0], 'name': r[1], 'dates_count': r[2]} for r in results]
        finally:
            db.close()

    def get_available_dates(self, client_code=None):
        """Retorna datas disponíveis (opcionalmente filtrado por cliente)"""
        db = SessionLocal()
        try:
            query = db.query(License.license_date)

            if client_code:
                query = query.filter(License.client_code == client_code)

            # Usar distinct() e group_by para garantir datas únicas
            dates = query.distinct().group_by(License.license_date).order_by(License.license_date.desc()).all()
            return [d[0] for d in dates]
        finally:
            db.close()

    def generate_txt_for_date_and_client(self, client_code, license_date):
        """Gera conteúdo TXT para um cliente e data específicos"""
        db = SessionLocal()
        try:
            # Buscar todas as licenças do cliente naquela data
            licenses = db.query(License).filter(
                License.client_code == client_code,
                License.license_date == license_date
            ).order_by(License.module_code).all()

            if not licenses:
                return None

            # Gerar conteúdo do TXT no formato original
            txt_lines = []
            for lic in licenses:
                # Formato: client_code,module_code,date,password,client_name
                line = f"{lic.client_code},{lic.module_code},{lic.license_date.strftime('%d/%m/%Y')},{lic.password},{lic.client_name}"
                txt_lines.append(line)

            return '\n'.join(txt_lines)
        finally:
            db.close()

    def search_licenses(self, client_code=None, license_date=None, limit=100):
        """Busca licenças com filtros"""
        db = SessionLocal()
        try:
            query = db.query(License)

            if client_code:
                query = query.filter(License.client_code == client_code)

            if license_date:
                query = query.filter(License.license_date == license_date)

            licenses = query.order_by(
                License.license_date.desc(),
                License.client_name,
                License.module_code
            ).limit(limit).all()

            return [lic.to_dict() for lic in licenses]
        finally:
            db.close()

    def get_licenses_by_client_and_date(self, client_code, license_date):
        """Retorna licenças agrupadas por cliente e data"""
        from app.models.license_application import LicenseApplication

        db = SessionLocal()
        try:
            licenses = db.query(License).filter(
                License.client_code == client_code,
                License.license_date == license_date
            ).order_by(License.module_code).all()

            if not licenses:
                return None

            # Criar lista de módulos descobrindo o nome real
            modules_data = []
            for lic in licenses:
                # O module_code contém: código_do_módulo + código_do_cliente
                # Exemplo: se module_code = "002123" e client_code = "123"
                # Então o código do módulo é "002"

                # Remover o código do cliente do final do module_code
                if lic.module_code.endswith(client_code):
                    pure_module_code = lic.module_code[:-len(client_code)]
                else:
                    pure_module_code = lic.module_code

                # Buscar o nome do módulo na tabela license_applications
                module_app = db.query(LicenseApplication).filter(
                    LicenseApplication.code == pure_module_code
                ).first()

                module_name = module_app.name if module_app else "NULL"

                modules_data.append({
                    'module_code': lic.module_code,
                    'module_name': module_name,
                    'password': lic.password
                })

            return {
                'client_code': client_code,
                'client_name': licenses[0].client_name if licenses else '',
                'license_date': license_date.strftime('%Y-%m-%d'),
                'modules': modules_data
            }
        finally:
            db.close()

    def delete_licenses_by_date(self, license_date):
        """Remove todas as licenças de uma data específica"""
        db = SessionLocal()
        try:
            deleted = db.query(License).filter(License.license_date == license_date).delete()
            db.commit()
            return deleted
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()


# Instância singleton do serviço
license_service = LicenseService()
