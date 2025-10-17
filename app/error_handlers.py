# -*- coding: utf-8 -*-
"""
Error handlers personalizados para a aplicação
"""
from flask import render_template
import traceback as tb
import os


def register_error_handlers(app):
    """Registra os error handlers na aplicação Flask"""

    @app.errorhandler(404)
    def page_not_found(error):
        """Handler para erro 404 - Página não encontrada"""
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handler para erro 500 - Erro interno do servidor"""
        # Obter detalhes do erro
        error_details = str(error)

        # Obter traceback completo apenas em desenvolvimento
        error_traceback = None
        if app.config.get('DEBUG') or os.getenv('FLASK_ENV') == 'development':
            error_traceback = tb.format_exc()

        return render_template(
            'errors/500.html',
            error_details=error_details,
            traceback=error_traceback
        ), 500

    @app.errorhandler(403)
    def forbidden(error):
        """Handler para erro 403 - Acesso negado"""
        return render_template(
            'errors/403.html',
            error_details=str(error)
        ), 403

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handler genérico para todas as exceções não tratadas"""
        # Log do erro
        app.logger.error(f'Exceção não tratada: {error}', exc_info=True)

        # Obter detalhes do erro
        error_details = str(error)

        # Obter traceback completo apenas em desenvolvimento
        error_traceback = None
        if app.config.get('DEBUG') or os.getenv('FLASK_ENV') == 'development':
            error_traceback = tb.format_exc()

        return render_template(
            'errors/500.html',
            error_details=error_details,
            traceback=error_traceback
        ), 500
