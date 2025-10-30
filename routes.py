from flask import Flask, Blueprint, session, redirect, url_for, flash
from functools import wraps
from app.controllers.auth import login_controller
from app.controllers.dashboard import dashboard_controller
from app.controllers.clients import clients_controller
from app.controllers.tickets import tickets_controller
from app.controllers.integrations import integrations_controller
from app.controllers import travels_controller
from app.controllers import profile_controller
from app.controllers import notifications_controller
from app.controllers import financial_controller
from app.controllers.settings import settings_controller
from app.controllers import notes_controller
from app.controllers.reports import reports_controller
from app.controllers.licenses import licenses_controller
from app.controllers.users import users_controller
from app.controllers.permissions import permissions_controller
from app.controllers.groups import groups_controller
from app.controllers.vehicles import vehicles_controller
from app.controllers import storage_controller
from app.utils.permissions_helper import inject_user_permissions


# Middleware de Autenticação
def login_required(f):
    """Decorator para proteger rotas que requerem autenticação"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta página', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return decorated_function


def register_routes(app: Flask):
    # Blueprint 1: Autenticação (rotas públicas)
    auth_bp = Blueprint('auth', __name__)

    auth_bp.add_url_rule('/', view_func=login_controller.index, methods=['GET'])
    auth_bp.add_url_rule('/login', view_func=login_controller.login, methods=['GET', 'POST'])
    auth_bp.add_url_rule('/logout', view_func=login_controller.logout, methods=['GET'])

    # Blueprint 2: Admin/Dashboard (rotas protegidas)
    admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

    # Middleware aplicado em todas as rotas do admin_bp
    @admin_bp.before_request
    def check_authentication():
        """Verifica autenticação antes de cada request no admin"""
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta página', 'warning')
            return redirect(url_for('auth.login'))

    admin_bp.add_url_rule('/dashboard', view_func=dashboard_controller.dashboard, methods=['GET'])

    # Rotas de Tickets
    admin_bp.add_url_rule('/tickets', view_func=tickets_controller.tickets_list, methods=['GET'])
    admin_bp.add_url_rule('/tickets/client/<int:client_id>', view_func=tickets_controller.tickets_view, methods=['GET'])

    # Rotas de Relatórios
    admin_bp.add_url_rule('/tickets/client/<int:client_id>/report/pdf', view_func=reports_controller.tickets_report_pdf, methods=['GET'])

    # Rotas de Clientes (Organizações)
    admin_bp.add_url_rule('/clients', view_func=clients_controller.clients_list, methods=['GET'])  # Lista de clientes
    admin_bp.add_url_rule('/clients/new', view_func=clients_controller.client_new, methods=['GET'])  # Formulário de novo cliente
    admin_bp.add_url_rule('/clients/create', view_func=clients_controller.client_create, methods=['POST'])
    admin_bp.add_url_rule('/clients/<int:client_id>/edit', view_func=clients_controller.client_edit, methods=['GET'])
    admin_bp.add_url_rule('/clients/<int:client_id>/update', view_func=clients_controller.client_update, methods=['POST'])
    admin_bp.add_url_rule('/clients/<int:client_id>/delete', view_func=clients_controller.client_delete, methods=['POST'])

    # APIs de Clientes
    admin_bp.add_url_rule('/api/organizations', view_func=clients_controller.get_organizations_api, methods=['GET'])
    admin_bp.add_url_rule('/api/clients', view_func=clients_controller.get_clients_api, methods=['GET'])
    admin_bp.add_url_rule('/api/applications', view_func=clients_controller.get_all_applications_api, methods=['GET'])
    admin_bp.add_url_rule('/api/clients/<int:client_id>/applications', view_func=clients_controller.get_applications_for_client_api, methods=['GET'])
    admin_bp.add_url_rule('/api/clients/<int:client_id>/applications/add', view_func=clients_controller.add_application_to_client_api, methods=['POST'])
    admin_bp.add_url_rule('/api/clients/<int:client_id>/applications/remove', view_func=clients_controller.remove_application_from_client_api, methods=['POST'])

    # Rotas de Integrações
    admin_bp.add_url_rule('/integrations', view_func=integrations_controller.integrations_list, methods=['GET'])
    admin_bp.add_url_rule('/integrations/movidesk', view_func=integrations_controller.movidesk_options, methods=['GET'])
    admin_bp.add_url_rule('/integrations/movidesk/tickets', view_func=integrations_controller.movidesk_tickets, methods=['GET'])
    admin_bp.add_url_rule('/integrations/movidesk/tickets/sync', view_func=integrations_controller.movidesk_sync_tickets, methods=['POST'])
    admin_bp.add_url_rule('/integrations/movidesk/organizations', view_func=integrations_controller.movidesk_organizations, methods=['GET'])
    admin_bp.add_url_rule('/integrations/movidesk/organizations/sync', view_func=integrations_controller.movidesk_sync_organizations, methods=['POST'])

    # Rotas de Viagens
    admin_bp.add_url_rule('/travels', view_func=travels_controller.travels_list, methods=['GET'])
    admin_bp.add_url_rule('/travels/new', view_func=travels_controller.travels_create, methods=['GET'])
    admin_bp.add_url_rule('/travels/create', view_func=travels_controller.travels_store, methods=['POST'])
    admin_bp.add_url_rule('/travels/<int:travel_id>/view', view_func=travels_controller.travels_view, methods=['GET'])
    admin_bp.add_url_rule('/travels/<int:travel_id>/edit', view_func=travels_controller.travels_edit, methods=['GET'])
    admin_bp.add_url_rule('/travels/<int:travel_id>/update', view_func=travels_controller.travels_update, methods=['POST'])
    admin_bp.add_url_rule('/travels/<int:travel_id>/delete', view_func=travels_controller.travels_delete, methods=['GET'])
    admin_bp.add_url_rule('/travels/<int:travel_id>/cancel', view_func=travels_controller.travels_cancel, methods=['GET'])
    admin_bp.add_url_rule('/travels/<int:travel_id>/analyze', view_func=travels_controller.travels_analyze, methods=['GET'])
    admin_bp.add_url_rule('/travels/<int:travel_id>/analyze/process', view_func=travels_controller.travels_analyze_process, methods=['POST'])

    # APIs de Viagens
    admin_bp.add_url_rule('/api/travels/vehicles', view_func=travels_controller.get_available_vehicles_api, methods=['GET'])

    # Rotas de Financeiro
    admin_bp.add_url_rule('/financial', view_func=financial_controller.financial_payouts_list, methods=['GET'])
    admin_bp.add_url_rule('/financial/<int:payout_id>/accountability', view_func=financial_controller.financial_accountability, methods=['GET'])
    admin_bp.add_url_rule('/financial/<int:payout_id>/accountability', view_func=financial_controller.save_accountability, methods=['POST'])
    admin_bp.add_url_rule('/financial/<int:payout_id>/review', view_func=financial_controller.financial_review_accountability, methods=['GET'])
    admin_bp.add_url_rule('/financial/<int:payout_id>/report/pdf', view_func=financial_controller.financial_accountability_report_pdf, methods=['GET'])

    # Rotas de Perfil
    admin_bp.add_url_rule('/profile', view_func=profile_controller.profile_view, methods=['GET'])
    admin_bp.add_url_rule('/profile/update', view_func=profile_controller.profile_update, methods=['POST'])

    # Rotas de Notificações
    admin_bp.add_url_rule('/notifications', view_func=notifications_controller.notifications_list, methods=['GET'])
    admin_bp.add_url_rule('/api/notifications', view_func=notifications_controller.notifications_api_list, methods=['GET'])
    admin_bp.add_url_rule('/api/notifications/unread-count', view_func=notifications_controller.get_unread_count, methods=['GET'])
    admin_bp.add_url_rule('/api/notifications/<int:notification_id>/read', view_func=notifications_controller.mark_as_read, methods=['POST'])
    admin_bp.add_url_rule('/api/notifications/read-all', view_func=notifications_controller.mark_all_as_read, methods=['POST'])
    admin_bp.add_url_rule('/api/notifications/<int:notification_id>/delete', view_func=notifications_controller.delete_notification, methods=['DELETE'])

    # Rotas de Edição de Organizações
    admin_bp.add_url_rule('/organizations/<string:org_id>/edit', view_func=integrations_controller.organization_edit, methods=['GET'])
    admin_bp.add_url_rule('/organizations/<string:org_id>/update', view_func=integrations_controller.organization_update, methods=['POST'])

    # APIs de Vinculação de Clientes
    admin_bp.add_url_rule('/api/clients/unlinked', view_func=integrations_controller.get_unlinked_clients, methods=['GET'])
    admin_bp.add_url_rule('/organizations/<string:org_id>/clients/<int:client_id>/link', view_func=integrations_controller.link_client_to_organization, methods=['POST'])
    admin_bp.add_url_rule('/organizations/<string:org_id>/clients/<int:client_id>/unlink', view_func=integrations_controller.unlink_client_from_organization, methods=['POST'])
    admin_bp.add_url_rule('/organizations/<string:org_id>/toggle-status', view_func=integrations_controller.toggle_organization_status, methods=['POST'])

    # Rotas de Configurações
    admin_bp.add_url_rule('/settings', view_func=settings_controller.settings_list, methods=['GET'])
    admin_bp.add_url_rule('/settings/update', view_func=settings_controller.settings_update, methods=['POST'])

    # API de Parâmetros
    admin_bp.add_url_rule('/api/parameters/<parameter_name>', view_func=settings_controller.get_parameter_api, methods=['GET'])
    admin_bp.add_url_rule('/api/parameters/<parameter_name>/update', view_func=settings_controller.update_parameter_api, methods=['POST'])

    # Rotas de Notes (Sticky Notes)
    admin_bp.add_url_rule('/notes', view_func=notes_controller.notes_list, methods=['GET'])

    # APIs de Notes
    admin_bp.add_url_rule('/api/notes', view_func=notes_controller.notes_api_list, methods=['GET'])
    admin_bp.add_url_rule('/api/notes/create', view_func=notes_controller.notes_create, methods=['POST'])
    admin_bp.add_url_rule('/api/notes/<int:note_id>/update', view_func=notes_controller.notes_update, methods=['PUT'])
    admin_bp.add_url_rule('/api/notes/<int:note_id>/delete', view_func=notes_controller.notes_delete, methods=['DELETE'])

    # Rotas de Licenças
    admin_bp.add_url_rule('/licenses', view_func=licenses_controller.licenses_list, methods=['GET'])
    admin_bp.add_url_rule('/licenses/upload/process', view_func=licenses_controller.license_upload_process, methods=['POST'])
    admin_bp.add_url_rule('/licenses/generate', view_func=licenses_controller.license_generate, methods=['GET'])
    admin_bp.add_url_rule('/licenses/generate-bulk', view_func=licenses_controller.license_generate_bulk, methods=['GET'])
    admin_bp.add_url_rule('/licenses/view', view_func=licenses_controller.license_view, methods=['GET'])
    admin_bp.add_url_rule('/licenses/view-pdf', view_func=licenses_controller.license_view_pdf, methods=['GET'])
    admin_bp.add_url_rule('/licenses/delete-date', view_func=licenses_controller.license_delete_date, methods=['POST'])
    admin_bp.add_url_rule('/licenses/modules', view_func=licenses_controller.license_modules_list, methods=['GET'])
    admin_bp.add_url_rule('/api/licenses/modules/create', view_func=licenses_controller.license_module_create, methods=['POST'])
    admin_bp.add_url_rule('/api/licenses/modules/update', view_func=licenses_controller.license_module_update, methods=['POST'])
    admin_bp.add_url_rule('/api/licenses/dates', view_func=licenses_controller.license_get_dates_api, methods=['GET'])

    # Rotas de Usuários
    admin_bp.add_url_rule('/users', view_func=users_controller.users_list, methods=['GET'])
    admin_bp.add_url_rule('/users/new', view_func=users_controller.user_new, methods=['GET'])
    admin_bp.add_url_rule('/users/create', view_func=users_controller.user_create, methods=['POST'])
    admin_bp.add_url_rule('/users/<int:user_id>/edit', view_func=users_controller.user_edit, methods=['GET'])
    admin_bp.add_url_rule('/users/<int:user_id>/update', view_func=users_controller.user_update, methods=['POST'])
    admin_bp.add_url_rule('/users/<int:user_id>/delete', view_func=users_controller.user_delete, methods=['POST'])

    # APIs de Usuários
    admin_bp.add_url_rule('/api/users', view_func=users_controller.get_users_api, methods=['GET'])

    # Rotas de Permissões
    admin_bp.add_url_rule('/permissions', view_func=permissions_controller.permissions_list, methods=['GET'])
    admin_bp.add_url_rule('/permissions/groups', view_func=permissions_controller.groups_permissions, methods=['GET'])
    admin_bp.add_url_rule('/permissions/groups/<int:group_id>/update', view_func=permissions_controller.group_permissions_update, methods=['POST'])
    admin_bp.add_url_rule('/api/permissions/groups/<int:group_id>', view_func=permissions_controller.api_group_permissions, methods=['GET'])
    admin_bp.add_url_rule('/api/permissions/by-module', view_func=permissions_controller.api_permissions_by_module, methods=['GET'])

    # Rotas de Grupos
    admin_bp.add_url_rule('/groups', view_func=groups_controller.groups_list, methods=['GET'])
    admin_bp.add_url_rule('/groups/new', view_func=groups_controller.groups_create, methods=['GET', 'POST'])
    admin_bp.add_url_rule('/groups/<int:group_id>/edit', view_func=groups_controller.groups_edit, methods=['GET', 'POST'])
    admin_bp.add_url_rule('/groups/<int:group_id>/delete', view_func=groups_controller.groups_delete, methods=['POST'])

    # Rotas de Veículos
    admin_bp.add_url_rule('/vehicles', view_func=vehicles_controller.vehicles_list, methods=['GET'])
    admin_bp.add_url_rule('/vehicles/new', view_func=vehicles_controller.vehicles_create, methods=['GET', 'POST'])
    admin_bp.add_url_rule('/vehicles/<int:vehicle_id>', view_func=vehicles_controller.vehicles_details, methods=['GET'])
    admin_bp.add_url_rule('/vehicles/<int:vehicle_id>/edit', view_func=vehicles_controller.vehicles_edit, methods=['GET', 'POST'])
    admin_bp.add_url_rule('/vehicles/<int:vehicle_id>/toggle-status', view_func=vehicles_controller.vehicles_toggle_status, methods=['POST'])

    # APIs de Configurações de Manutenção
    admin_bp.add_url_rule('/vehicles/<int:vehicle_id>/maintenance-configs', view_func=vehicles_controller.vehicles_add_maintenance_config, methods=['POST'])
    admin_bp.add_url_rule('/vehicles/<int:vehicle_id>/maintenance-configs/<int:config_id>', view_func=vehicles_controller.vehicles_remove_maintenance_config, methods=['DELETE'])

    # APIs do Storage Service
    admin_bp.add_url_rule('/api/storage/config', view_func=storage_controller.get_storage_config, methods=['GET'])
    admin_bp.add_url_rule('/api/storage/health', view_func=storage_controller.get_storage_health, methods=['GET'])
    admin_bp.add_url_rule('/api/storage/upload', view_func=storage_controller.upload_file, methods=['POST'])
    admin_bp.add_url_rule('/api/storage/<string:file_uuid>/view', view_func=storage_controller.download_file, methods=['GET'])
    admin_bp.add_url_rule('/api/storage/<string:file_uuid>/download', view_func=storage_controller.download_file, methods=['GET'])
    admin_bp.add_url_rule('/api/storage/<string:file_uuid>/delete', view_func=storage_controller.delete_file, methods=['DELETE'])
    admin_bp.add_url_rule('/api/storage/<string:file_uuid>', view_func=storage_controller.download_file, methods=['GET'])

    # Registrar Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # Context Processor para injetar prefixos nos templates
    @app.context_processor
    def inject_base_prefix():
        from flask import request
        prefixes = {
            'auth': '/',
            'admin': '/admin'
        }
        return {'base_prefix': prefixes.get(request.blueprint, '/')}

    # Context Processor para injetar permissões do usuário nos templates
    app.context_processor(inject_user_permissions)