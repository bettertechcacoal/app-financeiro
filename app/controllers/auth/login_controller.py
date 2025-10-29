from flask import render_template, request, redirect, url_for, session, flash
from app.services.auth_service import auth_service
from app.models.database import SessionLocal
from app.models.user import User


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

        # Primeiro, verificar se o usuário existe na base local
        db = SessionLocal()
        try:
            local_user = db.query(User).filter_by(email=email).first()

            if not local_user:
                flash('Usuário ou senha inválidos', 'error')
                return redirect(url_for('auth.login'))

            if not local_user.active:
                flash('Usuário inativo', 'error')
                return redirect(url_for('auth.login'))

            # Usuário existe localmente, agora autenticar via auth-service
            result = auth_service.login(email, password)

            if result:
                # Login bem-sucedido
                session['user_id'] = local_user.id
                session['user_name'] = local_user.name
                session['user_email'] = local_user.email
                session['access_token'] = result.get('access_token')
                session['refresh_token'] = result.get('refresh_token')

                return redirect(url_for('admin.dashboard'))
            else:
                flash('Email ou senha inválidos', 'error')
                return redirect(url_for('auth.login'))

        finally:
            db.close()

    return render_template('pages/auth/login.html')


def logout():
    """Logout do sistema"""
    session.clear()
    return redirect(url_for('auth.login'))