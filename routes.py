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
from app.controllers.settings import settings_controller
from app.controllers import notes_controller


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
    admin_bp.add_url_rule('/travels/<int:travel_id>/edit', view_func=travels_controller.travels_edit, methods=['GET'])
    admin_bp.add_url_rule('/travels/<int:travel_id>/update', view_func=travels_controller.travels_update, methods=['POST'])
    admin_bp.add_url_rule('/travels/<int:travel_id>/delete', view_func=travels_controller.travels_delete, methods=['GET'])
    admin_bp.add_url_rule('/travels/<int:travel_id>/approve', view_func=travels_controller.travels_approve, methods=['GET'])
    admin_bp.add_url_rule('/travels/<int:travel_id>/cancel', view_func=travels_controller.travels_cancel, methods=['GET'])

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
    admin_bp.add_url_rule('/settings/<int:parameter_id>/update', view_func=settings_controller.settings_update, methods=['POST'])

    # Rotas de Notes (Sticky Notes)
    admin_bp.add_url_rule('/notes', view_func=notes_controller.notes_list, methods=['GET'])
    admin_bp.add_url_rule('/notes/create', view_func=notes_controller.notes_create, methods=['POST'])
    admin_bp.add_url_rule('/notes/<int:note_id>/update', view_func=notes_controller.notes_update, methods=['POST', 'PUT'])
    admin_bp.add_url_rule('/notes/<int:note_id>/delete', view_func=notes_controller.notes_delete, methods=['POST', 'DELETE'])
    admin_bp.add_url_rule('/api/notes', view_func=notes_controller.notes_api_list, methods=['GET'])

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