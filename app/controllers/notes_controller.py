# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app.models.note import Note, NoteColor
from app.models.database import get_db
from sqlalchemy import desc


def notes_list():
    """Lista todas as notas do usuário"""
    db = get_db()
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('auth.login'))

    notes = db.query(Note).filter_by(user_id=user_id).order_by(desc(Note.created_at)).all()

    return render_template('pages/notes/list.html', notes=notes)


def notes_create():
    """Cria uma nova nota"""
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'success': False, 'message': 'Usuário não autenticado'}), 401

    if request.method == 'POST':
        db = get_db()

        try:
            data = request.get_json() if request.is_json else request.form

            note = Note(
                user_id=user_id,
                title=data.get('title'),
                content=data.get('content'),
                color=NoteColor[data.get('color', 'YELLOW').upper()],
                icon=data.get('icon', 'fa-sticky-note'),
                label=data.get('label', '')
            )

            db.add(note)
            db.commit()

            if request.is_json:
                return jsonify({'success': True, 'message': 'Nota criada com sucesso!', 'note_id': note.id})

            flash('Nota criada com sucesso!', 'success')
            return redirect(url_for('admin.dashboard'))

        except Exception as e:
            db.rollback()
            if request.is_json:
                return jsonify({'success': False, 'message': f'Erro ao criar nota: {str(e)}'}), 500

            flash(f'Erro ao criar nota: {str(e)}', 'error')
            return redirect(url_for('admin.dashboard'))


def notes_update(note_id):
    """Atualiza uma nota existente"""
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'success': False, 'message': 'Usuário não autenticado'}), 401

    db = get_db()
    note = db.query(Note).filter_by(id=note_id, user_id=user_id).first()

    if not note:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Nota não encontrada'}), 404
        flash('Nota não encontrada!', 'error')
        return redirect(url_for('admin.dashboard'))

    try:
        data = request.get_json() if request.is_json else request.form

        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        if data.get('color'):
            note.color = NoteColor[data.get('color').upper()]
        note.icon = data.get('icon', note.icon)
        note.label = data.get('label', note.label)

        db.commit()

        if request.is_json:
            return jsonify({'success': True, 'message': 'Nota atualizada com sucesso!'})

        flash('Nota atualizada com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))

    except Exception as e:
        db.rollback()
        if request.is_json:
            return jsonify({'success': False, 'message': f'Erro ao atualizar nota: {str(e)}'}), 500

        flash(f'Erro ao atualizar nota: {str(e)}', 'error')
        return redirect(url_for('admin.dashboard'))


def notes_delete(note_id):
    """Deleta uma nota"""
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'success': False, 'message': 'Usuário não autenticado'}), 401

    db = get_db()
    note = db.query(Note).filter_by(id=note_id, user_id=user_id).first()

    if not note:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Nota não encontrada'}), 404
        flash('Nota não encontrada!', 'error')
        return redirect(url_for('admin.dashboard'))

    try:
        db.delete(note)
        db.commit()

        if request.is_json:
            return jsonify({'success': True, 'message': 'Nota excluída com sucesso!'})

        flash('Nota excluída com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))

    except Exception as e:
        db.rollback()
        if request.is_json:
            return jsonify({'success': False, 'message': f'Erro ao excluir nota: {str(e)}'}), 500

        flash(f'Erro ao excluir nota: {str(e)}', 'error')
        return redirect(url_for('admin.dashboard'))


def notes_api_list():
    """API para listar notas (JSON)"""
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'success': False, 'message': 'Usuário não autenticado'}), 401

    db = get_db()
    limit = request.args.get('limit', type=int)

    query = db.query(Note).filter_by(user_id=user_id).order_by(desc(Note.created_at))

    if limit:
        query = query.limit(limit)

    notes = query.all()

    notes_data = [{
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'color': note.color.value,
        'icon': note.icon,
        'label': note.label,
        'created_at': note.created_at.isoformat() if note.created_at else None
    } for note in notes]

    total_count = db.query(Note).filter_by(user_id=user_id).count()

    return jsonify({
        'success': True,
        'notes': notes_data,
        'total': total_count
    })
