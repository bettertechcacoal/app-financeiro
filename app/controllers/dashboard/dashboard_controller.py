# -*- coding: utf-8 -*-
from flask import render_template, session


def dashboard():
    """Controller do dashboard principal"""
    user_name = session.get('user_name', 'Usuário')
    return render_template('pages/dashboard.html', user_name=user_name)
