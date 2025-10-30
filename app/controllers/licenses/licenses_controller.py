# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, jsonify, make_response, session
from app.services.license_service import license_service
from datetime import datetime
import threading


def licenses_list():
    """Lista de licenças e geração de TXT"""
    # Buscar clientes únicos
    clients = license_service.get_unique_clients()

    # Buscar datas disponíveis
    dates = license_service.get_available_dates()

    return render_template(
        'pages/licenses/list.html',
        clients=clients,
        dates=dates
    )


def license_upload_process():
    """Processa upload de arquivo TXT de forma assíncrona"""
    try:
        if 'file' not in request.files:
            flash('Nenhum arquivo foi enviado', 'error')
            return redirect(url_for('admin.licenses_list'))

        file = request.files['file']

        if file.filename == '':
            flash('Nenhum arquivo selecionado', 'error')
            return redirect(url_for('admin.licenses_list'))

        # Ler conteúdo do arquivo
        try:
            file_content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            # Tentar com latin-1 se utf-8 falhar
            file.seek(0)
            file_content = file.read().decode('latin-1')

        # Pegar user_id da sessão
        user_id = session.get('user_id')

        # Função que será executada em background
        def process_file_async(file_content, user_id):
            try:
                saved_count, dates_count = license_service.process_and_save_file(file_content)

                # Enviar notificação de sucesso
                if user_id:
                    from app.utils.notification_helper import send_notification
                    from app.models.notification import NotificationType
                    send_notification(
                        user_id=user_id,
                        title='Upload de Licenças Concluído',
                        message=f'{saved_count} licenças processadas com sucesso! ({dates_count} data(s) diferentes)',
                        notification_type=NotificationType.SUCCESS,
                        action_url='/admin/licenses',
                        action_text='Ver Licenças'
                    )

            except Exception as e:
                import traceback
                print(f"[ERRO] Erro ao processar arquivo: {str(e)}")
                print(traceback.format_exc())

                # Enviar notificação de erro
                if user_id:
                    from app.utils.notification_helper import send_notification
                    from app.models.notification import NotificationType
                    send_notification(
                        user_id=user_id,
                        title='Erro no Upload de Licenças',
                        message=f'Erro ao processar arquivo: {str(e)}',
                        notification_type=NotificationType.ERROR
                    )

        # Iniciar thread para processar em background
        thread = threading.Thread(target=process_file_async, args=(file_content, user_id))
        thread.daemon = True
        thread.start()

        # Retornar com flash message e voltar para lista
        flash('Arquivo enviado! O processamento está sendo executado em segundo plano. Você receberá uma notificação quando terminar.', 'info')
        return redirect(url_for('admin.licenses_list'))

    except Exception as e:
        import traceback
        print(f"[ERRO] Erro ao iniciar processamento: {str(e)}")
        print(traceback.format_exc())
        flash(f'Erro ao processar arquivo: {str(e)}', 'error')
        return redirect(url_for('admin.licenses_list'))


def license_generate():
    """Gera arquivo TXT para cliente e data selecionados"""
    try:
        client_code = request.args.get('client_code')
        license_date_str = request.args.get('license_date')

        if not client_code or not license_date_str:
            flash('Cliente e data são obrigatórios', 'error')
            return redirect(url_for('admin.licenses_list'))

        # Converter data
        license_date = datetime.strptime(license_date_str, '%Y-%m-%d').date()

        # Gerar TXT
        txt_content = license_service.generate_txt_for_date_and_client(client_code, license_date)

        if not txt_content:
            flash('Nenhuma licença encontrada para esse cliente e data', 'error')
            return redirect(url_for('admin.licenses_list'))

        # Buscar nome do cliente para o nome do arquivo
        clients = license_service.get_unique_clients()
        client_name = next((c['name'] for c in clients if c['code'] == client_code), client_code)

        # Preparar resposta com arquivo TXT
        response = make_response(txt_content)
        response.headers['Content-Type'] = 'text/plain; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename=senhas_{client_code}_{license_date.strftime("%d-%m-%Y")}.txt'

        return response

    except Exception as e:
        flash(f'Erro ao gerar arquivo: {str(e)}', 'error')
        return redirect(url_for('admin.licenses_list'))


def license_view():
    """Visualiza licenças de um cliente e data"""
    try:
        client_code = request.args.get('client_code')
        license_date_str = request.args.get('license_date')

        if not client_code or not license_date_str:
            flash('Cliente e data são obrigatórios', 'error')
            return redirect(url_for('admin.licenses_list'))

        # Converter data
        license_date = datetime.strptime(license_date_str, '%Y-%m-%d').date()

        # Buscar licenças
        license_data = license_service.get_licenses_by_client_and_date(client_code, license_date)

        if not license_data:
            flash('Nenhuma licença encontrada', 'error')
            return redirect(url_for('admin.licenses_list'))

        return render_template('pages/licenses/view.html', license=license_data)

    except Exception as e:
        flash(f'Erro ao visualizar licenças: {str(e)}', 'error')
        return redirect(url_for('admin.licenses_list'))


def license_get_dates_api():
    """API para buscar datas disponíveis (opcionalmente filtrado por cliente)"""
    try:
        client_code = request.args.get('client_code')

        # Se não passar client_code, retorna todas as datas disponíveis
        dates = license_service.get_available_dates(client_code)
        dates_str = [d.strftime('%Y-%m-%d') for d in dates]

        return jsonify({'success': True, 'dates': dates_str})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def license_generate_bulk():
    """Gera arquivo TXT único com múltiplos clientes"""
    try:
        # Receber lista de códigos de clientes (separados por vírgula)
        client_codes_str = request.args.get('client_codes')
        license_date_str = request.args.get('license_date')

        if not client_codes_str or not license_date_str:
            flash('Clientes e data são obrigatórios', 'error')
            return redirect(url_for('admin.licenses_list'))

        # Converter string de códigos para lista
        client_codes = [code.strip() for code in client_codes_str.split(',')]

        # Converter data
        license_date = datetime.strptime(license_date_str, '%Y-%m-%d').date()

        # Gerar TXT combinado
        all_lines = []
        clients_found = []

        for client_code in client_codes:
            txt_content = license_service.generate_txt_for_date_and_client(client_code, license_date)

            if txt_content:
                all_lines.append(txt_content)
                clients_found.append(client_code)

        if not all_lines:
            flash('Nenhuma licença encontrada para os clientes e data selecionados', 'error')
            return redirect(url_for('admin.licenses_list'))

        # Combinar todos os TXTs em um único arquivo
        combined_txt = '\n'.join(all_lines)

        # Nome do arquivo
        if len(clients_found) == 1:
            filename = f'senhas_{clients_found[0]}_{license_date.strftime("%d-%m-%Y")}.txt'
        else:
            filename = f'senhas_multiplos_clientes_{license_date.strftime("%d-%m-%Y")}.txt'

        # Preparar resposta
        response = make_response(combined_txt)
        response.headers['Content-Type'] = 'text/plain; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'

        return response

    except Exception as e:
        import traceback
        print(f"[ERRO] Erro ao gerar arquivo em massa: {str(e)}")
        print(traceback.format_exc())
        flash(f'Erro ao gerar arquivo: {str(e)}', 'error')
        return redirect(url_for('admin.licenses_list'))


def license_view_pdf():
    """Visualiza licenças em PDF (sem download)"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from io import BytesIO

        client_code = request.args.get('client_code')
        license_date_str = request.args.get('license_date')

        if not client_code or not license_date_str:
            return 'Cliente e data são obrigatórios', 400

        # Converter data
        license_date = datetime.strptime(license_date_str, '%Y-%m-%d').date()

        # Buscar licenças
        license_data = license_service.get_licenses_by_client_and_date(client_code, license_date)

        if not license_data:
            return 'Nenhuma licença encontrada', 404

        # Criar PDF em memória
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm, leftMargin=2*cm, rightMargin=2*cm)

        # Cores customizadas (tema pink do projeto)
        pink_header = colors.HexColor('#ec4899')  # Pink-500
        pink_dark = colors.HexColor('#db2777')    # Pink-600
        gray_light = colors.HexColor('#f9fafb')   # Gray-50
        gray_medium = colors.HexColor('#e5e7eb')  # Gray-200
        gray_dark = colors.HexColor('#374151')    # Gray-700
        gray_text = colors.HexColor('#6b7280')    # Gray-500

        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=pink_dark,
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=gray_dark,
            spaceAfter=20,
            alignment=TA_CENTER
        )

        # Elementos do PDF
        elements = []

        # Título
        title = Paragraph(f"LICENÇAS DE SISTEMA", title_style)
        elements.append(title)

        # Informações do cliente
        client_info = Paragraph(
            f"<b>Cliente:</b> {license_data['client_name']} | <b>Código:</b> {license_data['client_code']} | <b>Data:</b> {license_date.strftime('%d/%m/%Y')}",
            subtitle_style
        )
        elements.append(client_info)
        elements.append(Spacer(1, 0.7*cm))

        # Tabela de módulos
        table_data = [['CÓDIGO', 'NOME DO MÓDULO', 'SENHA']]

        for module in license_data['modules']:
            table_data.append([
                module['module_code'],
                module['module_name'],
                module['password']
            ])

        # Criar tabela
        table = Table(table_data, colWidths=[4*cm, 8.5*cm, 4.5*cm])
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), pink_header),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),

            # Corpo
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), gray_dark),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('LEFTPADDING', (0, 1), (-1, -1), 8),
            ('RIGHTPADDING', (0, 1), (-1, -1), 8),

            # Bordas suaves
            ('GRID', (0, 0), (-1, -1), 0.5, gray_medium),
            ('BOX', (0, 0), (-1, -1), 1, gray_medium),

            # Linhas alternadas
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, gray_light]),
        ]))

        elements.append(table)

        # Rodapé
        elements.append(Spacer(1, 1.2*cm))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=gray_text,
            alignment=TA_CENTER
        )
        footer = Paragraph(
            f"Documento gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
            footer_style
        )
        elements.append(footer)

        # Construir PDF
        doc.build(elements)

        # Retornar PDF
        buffer.seek(0)
        response = make_response(buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=licencas.pdf'

        return response

    except Exception as e:
        import traceback
        print(f"[ERRO] Erro ao gerar PDF: {str(e)}")
        print(traceback.format_exc())
        return f'Erro ao gerar PDF: {str(e)}', 500


def license_delete_date():
    """Remove todas as licenças de uma data específica"""
    try:
        license_date_str = request.form.get('license_date')

        if not license_date_str:
            flash('Data não fornecida', 'error')
            return redirect(url_for('admin.licenses_list'))

        license_date = datetime.strptime(license_date_str, '%Y-%m-%d').date()
        deleted = license_service.delete_licenses_by_date(license_date)

        flash(f'{deleted} licenças removidas com sucesso!', 'success')
        return redirect(url_for('admin.licenses_list'))

    except Exception as e:
        flash(f'Erro ao remover licenças: {str(e)}', 'error')
        return redirect(url_for('admin.licenses_list'))


def license_modules_list():
    """Lista todos os módulos cadastrados"""
    from app.models.database import SessionLocal
    from app.models.license_application import LicenseApplication

    db = SessionLocal()
    try:
        # Buscar todos os módulos ordenados por código
        modules = db.query(LicenseApplication).order_by(LicenseApplication.code).all()
        return render_template('pages/licenses/modules.html', modules=modules)
    finally:
        db.close()


def license_module_create():
    """Cria um novo módulo via AJAX"""
    from app.models.database import SessionLocal
    from app.models.license_application import LicenseApplication

    try:
        new_code = request.json.get('code')
        new_name = request.json.get('name')

        if not new_code or not new_name:
            return jsonify({'success': False, 'error': 'Dados incompletos'}), 400

        db = SessionLocal()
        try:
            # Verificar se já existe um módulo com esse código
            existing = db.query(LicenseApplication).filter(LicenseApplication.code == new_code.strip()).first()
            if existing:
                return jsonify({'success': False, 'error': 'Já existe um módulo com esse código'}), 400

            # Criar novo módulo
            new_module = LicenseApplication(
                code=new_code.strip(),
                name=new_name.strip()
            )
            db.add(new_module)
            db.commit()

            return jsonify({
                'success': True,
                'module': new_module.to_dict()
            })

        except Exception as e:
            db.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            db.close()

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def license_module_update():
    """Atualiza um módulo via AJAX"""
    from app.models.database import SessionLocal
    from app.models.license_application import LicenseApplication

    try:
        module_id = request.json.get('id')
        new_code = request.json.get('code')
        new_name = request.json.get('name')

        if not module_id or not new_code or not new_name:
            return jsonify({'success': False, 'error': 'Dados incompletos'}), 400

        db = SessionLocal()
        try:
            module = db.query(LicenseApplication).filter(LicenseApplication.id == module_id).first()

            if not module:
                return jsonify({'success': False, 'error': 'Módulo não encontrado'}), 404

            # Atualizar
            module.code = new_code.strip()
            module.name = new_name.strip()
            db.commit()

            return jsonify({
                'success': True,
                'module': module.to_dict()
            })

        except Exception as e:
            db.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            db.close()

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
