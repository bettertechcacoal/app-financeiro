from flask import render_template, request, redirect, url_for, session, flash
from app.services.auth_service import auth_service


def index():
    """Rota principal - redireciona para login ou dashboard"""
    if 'user_id' in session:
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('auth.login'))


def login():
    """Tela de login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')

        # Autenticar via auth-service
        result = auth_service.login(email, password)

        if result:
            # Login bem-sucedido
            user_data = result.get('user', {})
            session['user_id'] = user_data.get('id')
            session['user_name'] = user_data.get('name')
            session['user_email'] = user_data.get('email')
            session['access_token'] = result.get('access_token')
            session['refresh_token'] = result.get('refresh_token')

            return redirect(url_for('admin.dashboard'))
        else:
            flash('Email ou senha inválidos', 'error')
            return redirect(url_for('auth.login'))

    return render_template('pages/auth/login.html')


def logout():
    """Logout do sistema"""
    session.clear()
    return redirect(url_for('auth.login'))