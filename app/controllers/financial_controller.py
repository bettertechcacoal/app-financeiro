# -*- coding: utf-8 -*-
import logging
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app.models.database import SessionLocal
from app.models.travel_payout import TravelPayout
from app.models.travel_statement import TravelStatement, StatementStatus
from app.models.travel import Travel, TravelStatus
from app.models.user import User
from app.models.city import City
from app.models.state import State
from app.models.vehicle import Vehicle
from app.utils.permissions_helper import permission_required
from sqlalchemy.orm import joinedload
from sqlalchemy import case, func
import json


@permission_required('financial_accountability')
def financial_accountability(payout_id):
    """Exibe tela de prestação de contas (wizard)"""
    try:
        db = SessionLocal()

        # Obter ID do usuário logado
        user_id = session.get('user_id')

        if not user_id:
            flash('Usuário não autenticado', 'error')
            return redirect(url_for('auth.login'))

        # Buscar o payout do usuário logado
        from app.models.vehicle_travel_history import VehicleTravelHistory
        from app.models.vehicle import Vehicle

        payout = db.query(TravelPayout)\
            .filter_by(id=payout_id, member_id=user_id)\
            .join(Travel)\
            .options(
                joinedload(TravelPayout.travel).joinedload(Travel.city).joinedload(City.state),
                joinedload(TravelPayout.travel).joinedload(Travel.driver_user),
                joinedload(TravelPayout.travel).joinedload(Travel.vehicle_history).joinedload(VehicleTravelHistory.vehicle)
            )\
            .first()

        if not payout:
            flash('Repasse não encontrado ou você não tem permissão para acessá-lo', 'error')
            return redirect(url_for('admin.financial_payouts_list'))

        payout_data = payout.to_dict()

        # Buscar prestação de contas existente (se houver)
        existing_statement = db.query(TravelStatement).filter_by(payout_id=payout_id).first()
        if existing_statement:
            payout_data['existing_statement'] = existing_statement.to_dict()
        else:
            payout_data['existing_statement'] = None

        # Adicionar informações da viagem
        if payout.travel:
            # Pegar o veículo alocado (se houver) do histórico
            allocated_vehicle = None
            if payout.travel.vehicle_history:
                # Pegar o último registro de veículo para esta viagem
                last_vehicle_history = payout.travel.vehicle_history[-1] if payout.travel.vehicle_history else None
                if last_vehicle_history and last_vehicle_history.vehicle:
                    allocated_vehicle = last_vehicle_history.vehicle.to_dict()

            payout_data['travel_info'] = {
                'id': payout.travel.id,
                'purpose': payout.travel.purpose,
                'departure_date': payout.travel.departure_date.isoformat() if payout.travel.departure_date else None,
                'return_date': payout.travel.return_date.isoformat() if payout.travel.return_date else None,
                'status': payout.travel.status.value if payout.travel.status else None,
                'city': payout.travel.city.to_dict() if payout.travel.city else None,
                'driver_user': payout.travel.driver_user.to_dict() if payout.travel.driver_user else None,
                'vehicle': allocated_vehicle
            }

        db.close()

        return render_template(
            'pages/financial/accountability.html',
            payout=payout_data
        )

    except Exception as e:
        logging.error(f"Erro ao carregar prestação de contas: {e}")
        flash('Erro ao carregar prestação de contas', 'error')
        return redirect(url_for('admin.financial_payouts_list'))


def financial_payouts_list():
    """Lista todos os repasses financeiros do usuário logado ou todos se tiver permissão"""
    try:
        db = SessionLocal()

        # Obter ID do usuário logado
        user_id = session.get('user_id')

        if not user_id:
            flash('Usuário não autenticado', 'error')
            return redirect(url_for('auth.login'))

        # Verificar se usuário tem permissão para ver todos os registros
        from app.utils.permissions_helper import user_has_permission
        can_review_all = user_has_permission('financial_review_accountability')

        # Buscar todos os payouts com relacionamentos
        # Fazer LEFT JOIN com travel_statements para pegar o status da prestação de contas
        from sqlalchemy.orm import outerjoin

        query = db.query(TravelPayout, TravelStatement.status)\
            .outerjoin(TravelStatement, TravelPayout.id == TravelStatement.payout_id)\
            .join(Travel, TravelPayout.travel_id == Travel.id)\
            .filter(Travel.status != TravelStatus.CANCELLED)\
            .options(
                joinedload(TravelPayout.travel).joinedload(Travel.city).joinedload(City.state),
                joinedload(TravelPayout.travel).joinedload(Travel.driver_user),
                joinedload(TravelPayout.member)
            )

        if not can_review_all:
            query = query.filter(TravelPayout.member_id == user_id)
        else:
            from sqlalchemy import or_, and_
            from datetime import datetime

            # Data atual para comparar com data de retorno
            today = datetime.now().date()

            query = query.filter(
                or_(
                    # Seus próprios repasses
                    TravelPayout.member_id == user_id,
                    # Repasses já enviados ou aprovados
                    TravelStatement.status.in_([StatementStatus.APPROVED, StatementStatus.SUBMITTED]),
                    # Repasses cuja data de retorno já passou (independente do status)
                    and_(
                        Travel.return_date.isnot(None),
                        Travel.return_date < today
                    )
                )
            )

        payouts = query.order_by(TravelPayout.created_at.desc()).all()

        # Converter para dicionários
        payouts_data = []
        for payout, statement_status in payouts:
            payout_dict = payout.to_dict()

            # Substituir o status do payout pelo status da prestação de contas
            # Se não houver prestação de contas, usar 'draft' como padrão (pendente)
            if statement_status:
                payout_dict['accountability_status'] = statement_status.value
            else:
                payout_dict['accountability_status'] = 'draft'  # Pendente por padrão

            # Adicionar informações da viagem
            if payout.travel:
                payout_dict['travel_info'] = {
                    'id': payout.travel.id,
                    'purpose': payout.travel.purpose,
                    'departure_date': payout.travel.departure_date.isoformat() if payout.travel.departure_date else None,
                    'return_date': payout.travel.return_date.isoformat() if payout.travel.return_date else None,
                    'status': payout.travel.status.value if payout.travel.status else None,
                    'city': payout.travel.city.to_dict() if payout.travel.city else None,
                    'driver_user': payout.travel.driver_user.to_dict() if payout.travel.driver_user else None
                }
            payouts_data.append(payout_dict)

        # Calcular totais
        total_all = sum(p['amount'] for p in payouts_data)

        db.close()

        return render_template(
            'pages/financial/list.html',
            payouts=payouts_data,
            total_payouts=len(payouts_data),
            total_all=total_all
        )

    except Exception as e:
        logging.error(f"Erro ao listar repasses financeiros: {e}")
        flash('Erro ao carregar lista de repasses financeiros', 'error')
        return redirect(url_for('admin.dashboard'))


@permission_required('financial_review_accountability')
def financial_review_accountability(payout_id):
    """Exibe tela de análise/revisão da prestação de contas"""
    db = SessionLocal()

    # Obter ID do usuário logado
    user_id = session.get('user_id')

    if not user_id:
        flash('Usuário não autenticado', 'error')
        return redirect(url_for('auth.login'))

    # Buscar o payout (sem filtro de member_id pois analista pode ver qualquer prestação)
    from app.models.vehicle_travel_history import VehicleTravelHistory
    from app.models.vehicle import Vehicle

    payout = db.query(TravelPayout)\
        .filter_by(id=payout_id)\
        .join(Travel)\
        .options(
            joinedload(TravelPayout.travel).joinedload(Travel.city).joinedload(City.state),
            joinedload(TravelPayout.travel).joinedload(Travel.driver_user),
            joinedload(TravelPayout.travel).joinedload(Travel.vehicle_history).joinedload(VehicleTravelHistory.vehicle),
            joinedload(TravelPayout.member)
        )\
        .first()

    if not payout:
        db.close()
        flash('Repasse não encontrado', 'error')
        return redirect(url_for('admin.financial_payouts_list'))

    # Buscar prestação de contas
    statement = db.query(TravelStatement).filter_by(payout_id=payout_id).first()

    if not statement:
        db.close()
        flash('Prestação de contas não encontrada', 'warning')
        return redirect(url_for('admin.financial_payouts_list'))

    payout_data = payout.to_dict()
    payout_data['statement'] = statement.to_dict()

    # Adicionar informações da viagem
    if payout.travel:
        # Pegar o veículo alocado (se houver) do histórico
        allocated_vehicle = None
        if payout.travel.vehicle_history:
            last_vehicle_history = payout.travel.vehicle_history[-1] if payout.travel.vehicle_history else None
            if last_vehicle_history and last_vehicle_history.vehicle:
                allocated_vehicle = last_vehicle_history.vehicle.to_dict()

        payout_data['travel_info'] = {
            'id': payout.travel.id,
            'purpose': payout.travel.purpose,
            'departure_date': payout.travel.departure_date.isoformat() if payout.travel.departure_date else None,
            'return_date': payout.travel.return_date.isoformat() if payout.travel.return_date else None,
            'status': payout.travel.status.value if payout.travel.status else None,
            'city': payout.travel.city.to_dict() if payout.travel.city else None,
            'driver_user': payout.travel.driver_user.to_dict() if payout.travel.driver_user else None,
            'vehicle': allocated_vehicle
        }

    db.close()

    return render_template(
        'pages/financial/review.html',
        payout=payout_data
    )


def save_accountability(payout_id):
    """Salva ou atualiza a prestação de contas"""
    try:
        db = SessionLocal()
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({'success': False, 'error': 'Usuário não autenticado'}), 401

        # Obter dados JSON do request
        data = request.get_json()
        statement_content = data.get('statement_content', {})
        status = data.get('status', 'draft')  # Status padrão é 'draft'

        # Validar status e converter para enum
        status_map = {
            'draft': StatementStatus.DRAFT,
            'submitted': StatementStatus.SUBMITTED,
            'returned': StatementStatus.RETURNED,
            'approved': StatementStatus.APPROVED
        }

        if status not in status_map:
            db.close()
            return jsonify({'success': False, 'error': 'Status inválido'}), 400

        status_enum = status_map[status]

        # Verificar permissão baseada no status da operação
        from app.utils.permissions_helper import user_has_permission

        # Para aprovação ou devolução, apenas verificar permissão
        if status in ['approved', 'returned']:
            if not user_has_permission('financial_review_accountability'):
                db.close()
                return jsonify({'success': False, 'error': 'Você não tem permissão para esta ação'}), 403
            # Buscar payout sem filtro de member_id
            payout = db.query(TravelPayout).filter_by(id=payout_id).first()
        else:
            # Para rascunho ou envio, usuário deve ser o dono
            payout = db.query(TravelPayout).filter_by(id=payout_id, member_id=user_id).first()

        if not payout:
            db.close()
            return jsonify({'success': False, 'error': 'Repasse não encontrado'}), 404

        # Buscar ou criar prestação de contas
        statement = db.query(TravelStatement).filter_by(payout_id=payout_id).first()

        if statement:
            # Atualizar existente
            logging.debug(f"Atualizando statement existente ID: {statement.id}")
            statement.statement_content = statement_content
            statement.status = status_enum
        else:
            # Criar nova
            logging.debug(f"Criando nova statement para payout_id: {payout_id}")
            statement = TravelStatement(
                payout_id=payout_id,
                statement_content=statement_content,
                status=status_enum
            )
            db.add(statement)

        db.commit()
        db.refresh(statement)

        # Mensagem de sucesso baseada no status
        messages = {
            'draft': 'Rascunho salvo com sucesso!',
            'submitted': 'Prestação de contas enviada com sucesso!',
            'returned': 'Prestação de contas retornada para revisão',
            'approved': 'Prestação de contas aprovada!'
        }

        statement_id = statement.id
        db.close()

        return jsonify({
            'success': True,
            'message': messages.get(status, 'Prestação de contas salva com sucesso!'),
            'statement_id': statement_id
        })

    except Exception as e:
        if db:
            db.rollback()
            db.close()
        logging.error(f"Erro ao salvar prestação de contas: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


def financial_accountability_report_pdf(payout_id):
    """Gera relatório de prestação de contas em PDF"""
    from flask import make_response
    from datetime import datetime
    from io import BytesIO
    import os
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

    db = SessionLocal()

    try:
        # Buscar informações do repasse e prestação de contas
        from app.models.vehicle_travel_history import VehicleTravelHistory

        user_id = session.get('user_id')
        payout = db.query(TravelPayout).options(
            joinedload(TravelPayout.member),
            joinedload(TravelPayout.travel).joinedload(Travel.city).joinedload(City.state),
            joinedload(TravelPayout.travel).joinedload(Travel.vehicle_history).joinedload(VehicleTravelHistory.vehicle)
        ).filter(TravelPayout.id == payout_id).first()

        if not payout:
            return "Repasse não encontrado", 404

        # Buscar prestação de contas separadamente
        statement = db.query(TravelStatement).filter_by(payout_id=payout_id).first()

        if not statement:
            return "Prestação de contas não encontrada", 404

        statement_data = statement.statement_content

        # Gerar PDF
        buffer = BytesIO()
        pdf = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2.5*cm,
            leftMargin=2.5*cm,
            topMargin=0.8*cm,
            bottomMargin=2*cm,
            title='Relatório'
        )

        # Estilos
        styles = getSampleStyleSheet()

        style_header = ParagraphStyle(
            'Header',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.black,
            alignment=TA_CENTER,
            spaceAfter=0.1*cm,
            leading=12
        )

        style_title = ParagraphStyle(
            'Title',
            parent=styles['Normal'],
            fontSize=16,
            fontName='Helvetica-Bold',
            textColor=colors.black,
            alignment=TA_CENTER,
            spaceAfter=0.8*cm
        )

        style_section = ParagraphStyle(
            'Section',
            parent=styles['Normal'],
            fontSize=12,
            fontName='Helvetica-Bold',
            textColor=colors.black,
            alignment=TA_LEFT,
            spaceAfter=0.4*cm,
            spaceBefore=0.6*cm
        )

        style_body = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            alignment=TA_LEFT,
            spaceAfter=0.3*cm
        )

        # Conteúdo
        story = []

        # LOGO DA EMPRESA
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        logo_path = os.path.join(base_dir, 'static', 'images', 'letterhead_logo.png')
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=6*cm, height=3*cm, kind='proportional')
            logo.hAlign = 'CENTER'
            story.append(logo)
            story.append(Spacer(1, 0.3*cm))

        # CABEÇALHO
        story.append(Paragraph("<b>BETTER TECH INFORMÁTICA, SERVIÇOS DE AUTOMAÇÃO LTDA.</b>", style_header))
        story.append(Paragraph("Rua Leonório Perdocini, nº 1997 • Bairro Eldorado • CEP 76.966-192 • Cacoal/RO", style_header))
        story.append(Paragraph("CNPJ: 07.114.391/0001-14 • Telefone: (69) 3441-1304 • E-mail: contato@bettertech.com.br", style_header))
        story.append(Spacer(1, 0.8*cm))

        # TÍTULO
        story.append(Paragraph("<b>RELATÓRIO DE PRESTAÇÃO DE CONTAS</b>", style_title))
        story.append(Spacer(1, 0.5*cm))

        # Calcular valores a devolver e receber
        from decimal import Decimal
        total_food_calc = Decimal(str(statement_data.get('food', {}).get('amount', 0)))
        total_vehicle_calc = Decimal(str(statement_data.get('vehicle', {}).get('amount', 0)))
        total_lodging_calc = Decimal(str(statement_data.get('lodging', {}).get('amount', 0)))
        total_other_calc = Decimal(str(statement_data.get('other', {}).get('amount', 0)))
        total_general_calc = total_food_calc + total_vehicle_calc + total_lodging_calc + total_other_calc
        saldo_calc = payout.amount - total_general_calc

        if saldo_calc > 0:
            valor_devolver = saldo_calc
            valor_receber = 0
        elif saldo_calc < 0:
            valor_devolver = 0
            valor_receber = abs(saldo_calc)
        else:
            valor_devolver = 0
            valor_receber = 0

        # Tabela de Informações do Colaborador (Nº, Nome, Saldo Devedor e Saldo Reembolso) - NO TOPO
        member_info_data = [
            ['Nº:', str(payout.member.id).zfill(5) if payout.member else 'N/A'],  # Linha 1: Nº e valor (5 dígitos)
            ['Nome:', payout.member.name if payout.member else 'N/A'],   # Linha 2: Nome e valor
            ['Saldo Devedor:', f"R$ {valor_devolver:.2f}".replace('.', ','),
             'Saldo Reembolso:', f"R$ {valor_receber:.2f}".replace('.', ',')]  # Linha 3: 4 colunas
        ]

        member_table = Table(member_info_data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
        member_table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
            ('BACKGROUND', (0, 0), (0, 1), colors.HexColor('#f3f4f6')),  # Background dos labels Nº e Nome
            ('FONTNAME', (0, 0), (0, 1), 'Helvetica-Bold'),  # Labels Nº e Nome em negrito
            ('FONTNAME', (1, 0), (3, 0), 'Helvetica-Bold'),  # Valor do Nº em negrito
            ('SPAN', (1, 0), (3, 0)),  # Linha 1: valor do Nº ocupa 3 colunas
            ('SPAN', (1, 1), (3, 1)),  # Linha 2: valor do Nome ocupa 3 colunas
            ('BACKGROUND', (0, 2), (0, 2), colors.HexColor('#f3f4f6')),  # Background do label Valores a Devolver
            ('BACKGROUND', (2, 2), (2, 2), colors.HexColor('#f3f4f6')),  # Background do label Valores a Receber
            ('FONTNAME', (0, 2), (0, 2), 'Helvetica-Bold'),  # Valores a Devolver em negrito
            ('FONTNAME', (2, 2), (2, 2), 'Helvetica-Bold'),  # Valores a Receber em negrito
            ('ALIGN', (1, 2), (1, 2), 'RIGHT'),  # Alinhar valor a devolver à direita
            ('ALIGN', (3, 2), (3, 2), 'RIGHT'),  # Alinhar valor a receber à direita
        ]))
        story.append(member_table)
        story.append(Spacer(1, 0.5*cm))

        # Informações da Viagem
        if payout.travel:
            story.append(Paragraph("<b>INFORMAÇÕES DA VIAGEM</b>", style_section))

            # Pegar veículo do histórico
            vehicle_info = 'N/A'
            if payout.travel.vehicle_history and len(payout.travel.vehicle_history) > 0:
                vehicle = payout.travel.vehicle_history[-1].vehicle
                if vehicle:
                    vehicle_info = f"{vehicle.plate} ({vehicle.model})"

            # Pegar quilometragem do statement_content
            km_saida = 'N/A'
            km_chegada = 'N/A'
            km_total = 'N/A'

            if statement_data.get('vehicle'):
                vehicle_data = statement_data['vehicle']
                km_start = vehicle_data.get('km_start', 0)
                km_end = vehicle_data.get('km_end', 0)
                km_traveled = vehicle_data.get('km_traveled', 0)

                if km_start is not None and km_start > 0:
                    km_saida = f"{km_start:,} km".replace(',', '.')
                if km_end is not None and km_end > 0:
                    km_chegada = f"{km_end:,} km".replace(',', '.')
                if km_traveled is not None and km_traveled > 0:
                    km_total = f"{km_traveled:,} km".replace(',', '.')

            travel_info = [
                ['Destino:', payout.travel.city.name if payout.travel.city else 'N/A', '', ''],
                ['Veículo:', vehicle_info, '', ''],
                ['Saída:', payout.travel.departure_date.strftime('%d/%m/%Y') if payout.travel.departure_date else 'N/A', 'Chegada:', payout.travel.return_date.strftime('%d/%m/%Y') if payout.travel.return_date else 'N/A'],
                ['KM Saída:', km_saida, 'KM Chegada:', km_chegada],
                ['KM Percorrido:', km_total, '', '']
            ]

            table = Table(travel_info, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
            table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),  # Primeira coluna em negrito
                ('FONTNAME', (2, 2), (2, 3), 'Helvetica-Bold'),  # Terceira coluna linhas 2 e 3 em negrito
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),  # Fundo cinza claro para labels
                ('BACKGROUND', (2, 2), (2, 3), colors.HexColor('#f3f4f6')),  # Fundo cinza claro para labels das linhas 2 e 3
                ('SPAN', (1, 0), (3, 0)),  # Mesclar colunas 1-3 na linha 0 (Destino)
                ('SPAN', (1, 1), (3, 1)),  # Mesclar colunas 1-3 na linha 1 (Veículo)
                ('SPAN', (1, 4), (3, 4)),  # Mesclar colunas 1-3 na linha 4 (Total Percorrido)
            ]))
            story.append(table)

        # ALIMENTAÇÃO
        story.append(Paragraph("<b>ALIMENTAÇÃO</b>", style_section))
        if statement_data.get('food') and statement_data['food'].get('days'):
            food_data = [['DATA', 'DESCRIÇÃO', 'VALOR']]
            for day in statement_data['food']['days']:
                meals = ', '.join([m['name'] for m in day.get('meals', [])])
                food_data.append([
                    day.get('date_formatted', ''),
                    meals,
                    f"R$ {day.get('amount', 0):.2f}".replace('.', ',')
                ])

            food_data.append([Paragraph('<b>Total</b>', getSampleStyleSheet()['Normal']), '', f"R$ {statement_data['food'].get('amount', 0):.2f}".replace('.', ',')])

            table = Table(food_data, colWidths=[3*cm, 10*cm, 3*cm])
            table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e5e7eb')),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f9fafb')),
                ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
                ('SPAN', (0, -1), (1, -1)),  # Mesclar primeira e segunda coluna na última linha
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, -1), (0, -1), 'RIGHT'),
            ]))
            story.append(table)
        else:
            empty_msg = Paragraph('Não há despesas registradas', getSampleStyleSheet()['Normal'])
            empty_table = Table([[empty_msg]], colWidths=[16*cm])
            empty_table.setStyle(TableStyle([
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#6b7280')),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9fafb')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(empty_table)

        # VEÍCULO
        story.append(Paragraph("<b>VEÍCULO</b>", style_section))
        if statement_data.get('vehicle') and statement_data['vehicle'].get('expenses'):
            vehicle_data = [['DATA', 'DESCRIÇÃO', 'VALOR']]
            for expense in statement_data['vehicle']['expenses']:
                vehicle_data.append([
                    expense.get('date_formatted', ''),
                    expense.get('name', ''),
                    f"R$ {expense.get('amount', 0):.2f}".replace('.', ',')
                ])

            vehicle_data.append([Paragraph('<b>Total</b>', getSampleStyleSheet()['Normal']), '', f"R$ {statement_data['vehicle'].get('amount', 0):.2f}".replace('.', ',')])

            table = Table(vehicle_data, colWidths=[3*cm, 10*cm, 3*cm])
            table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e5e7eb')),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f9fafb')),
                ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
                ('SPAN', (0, -1), (1, -1)),  # Mesclar primeira e segunda coluna na última linha
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, -1), (0, -1), 'RIGHT'),
            ]))
            story.append(table)
        else:
            empty_msg = Paragraph('Não há despesas registradas', getSampleStyleSheet()['Normal'])
            empty_table = Table([[empty_msg]], colWidths=[16*cm])
            empty_table.setStyle(TableStyle([
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#6b7280')),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9fafb')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(empty_table)

        # HOSPEDAGEM
        story.append(Paragraph("<b>HOSPEDAGEM</b>", style_section))
        if statement_data.get('lodging') and statement_data['lodging'].get('expenses'):
            lodging_data = [['DATA', 'DESCRIÇÃO', 'VALOR']]
            for expense in statement_data['lodging']['expenses']:
                lodging_data.append([
                    expense.get('date_formatted', ''),
                    expense.get('name', 'Hospedagem'),
                    f"R$ {expense.get('amount', 0):.2f}".replace('.', ',')
                ])

            lodging_data.append([Paragraph('<b>Total</b>', getSampleStyleSheet()['Normal']), '', f"R$ {statement_data['lodging'].get('amount', 0):.2f}".replace('.', ',')])

            table = Table(lodging_data, colWidths=[3*cm, 10*cm, 3*cm])
            table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e5e7eb')),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f9fafb')),
                ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
                ('SPAN', (0, -1), (1, -1)),  # Mesclar primeira e segunda coluna na última linha
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, -1), (0, -1), 'RIGHT'),
            ]))
            story.append(table)
        else:
            empty_msg = Paragraph('Não há despesas registradas', getSampleStyleSheet()['Normal'])
            empty_table = Table([[empty_msg]], colWidths=[16*cm])
            empty_table.setStyle(TableStyle([
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#6b7280')),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9fafb')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(empty_table)

        # OUTRAS DESPESAS
        story.append(Paragraph("<b>OUTRAS DESPESAS</b>", style_section))
        if statement_data.get('other') and statement_data['other'].get('expenses'):
            other_data = [['DATA', 'DESCRIÇÃO', 'VALOR']]
            for expense in statement_data['other']['expenses']:
                other_data.append([
                    expense.get('date_formatted', ''),
                    expense.get('description', ''),
                    f"R$ {expense.get('amount', 0):.2f}".replace('.', ',')
                ])

            other_data.append([Paragraph('<b>Total</b>', getSampleStyleSheet()['Normal']), '', f"R$ {statement_data['other'].get('amount', 0):.2f}".replace('.', ',')])

            table = Table(other_data, colWidths=[3*cm, 10*cm, 3*cm])
            table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e5e7eb')),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f9fafb')),
                ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
                ('SPAN', (0, -1), (1, -1)),  # Mesclar primeira e segunda coluna na última linha
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, -1), (0, -1), 'RIGHT'),
            ]))
            story.append(table)
        else:
            empty_msg = Paragraph('Não há despesas registradas', getSampleStyleSheet()['Normal'])
            empty_table = Table([[empty_msg]], colWidths=[16*cm])
            empty_table.setStyle(TableStyle([
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#6b7280')),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9fafb')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(empty_table)

        # TOTALIZADOR
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph("<b>RESUMO FINANCEIRO</b>", style_section))

        total_food = Decimal(str(statement_data.get('food', {}).get('amount', 0)))
        total_vehicle = Decimal(str(statement_data.get('vehicle', {}).get('amount', 0)))
        total_lodging = Decimal(str(statement_data.get('lodging', {}).get('amount', 0)))
        total_other = Decimal(str(statement_data.get('other', {}).get('amount', 0)))
        total_general = total_food + total_vehicle + total_lodging + total_other
        saldo = payout.amount - total_general

        summary_data = [
            ['Repasse:', f"R$ {payout.amount:.2f}".replace('.', ',')],
            ['Despesa:', f"R$ {total_general:.2f}".replace('.', ',')],
            ['Saldo Final:', f"R$ {saldo:.2f}".replace('.', ',')],
        ]

        table = Table(summary_data, colWidths=[10*cm, 6*cm])
        table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (1, 0), (1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e5e7eb')),  # Saldo Final
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        story.append(table)

        # Rodapé
        def add_page_number(canvas, doc):
            page_num = canvas.getPageNumber()
            canvas.setStrokeColor(colors.HexColor('#CCCCCC'))
            canvas.setLineWidth(0.5)
            canvas.line(2.5*cm, 1.5*cm, A4[0] - 2.5*cm, 1.5*cm)
            canvas.setFont('Helvetica', 7)
            canvas.setFillColor(colors.HexColor('#333333'))
            canvas.drawString(2.5*cm, 1*cm, "Rua Leonório Perdocini, nº 1997, Cacoal/RO")
            canvas.drawCentredString(A4[0] / 2, 1*cm, f"Página {page_num}")
            canvas.drawRightString(A4[0] - 2.5*cm, 1*cm, "(69) 3441-1304")

        pdf.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)

        buffer.seek(0)
        response = make_response(buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=prestacao_contas_repasse_{payout_id}.pdf'

        return response

    except Exception as e:
        logging.error(f"Erro ao gerar relatório: {e}")
        return f"Erro ao gerar relatório: {str(e)}", 500
    finally:
        db.close()
