# -*- coding: utf-8 -*-
from flask import make_response, request
from datetime import datetime, timedelta
from io import BytesIO
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

from app.services.client_service import client_service
from app.services.ticket_service import ticket_service
from app.models.client_organization import ClientOrganization
from app.models.organization import Organization
from app.models.application_ticket_module import ApplicationTicketModule
from app.models.ticket_module import TicketModule
from app.models.client_application import ClientApplication
from app.models.database import db_session


def add_page_number(canvas, doc):
    """Adiciona rodapé e número de página em todas as páginas"""
    page_num = canvas.getPageNumber()

    # Linha decorativa fina acima do rodapé
    canvas.setStrokeColor(colors.HexColor('#CCCCCC'))
    canvas.setLineWidth(0.5)
    canvas.line(2.5*cm, 1.5*cm, A4[0] - 2.5*cm, 1.5*cm)

    # Informações do rodapé
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(colors.HexColor('#333333'))

    # Endereço à esquerda
    text = "Rua Leonório Perdocini, nº 1997, Cacoal/RO"
    canvas.drawString(2.5*cm, 1*cm, text)

    # Número da página centralizado
    text = f"Página {page_num}"
    canvas.drawCentredString(A4[0] / 2, 1*cm, text)

    # Telefone à direita
    text = "(69) 3441-1304"
    canvas.drawRightString(A4[0] - 2.5*cm, 1*cm, text)


def tickets_report_pdf(client_id):
    """Gera relatório de serviço em PDF no formato de ofício"""
    # Parâmetros da requisição
    month = int(request.args.get('month', datetime.now().month))
    year = int(request.args.get('year', datetime.now().year))
    oficio_number_custom = request.args.get('oficio_number', '')
    invoice_number = request.args.get('invoice_number', '')

    # Buscar cliente
    client = client_service.get_client_by_id(client_id)
    if not client:
        return "Cliente não encontrado", 404

    # Calcular período baseado no ciclo de cobrança
    start_date, end_date = calculate_billing_period(client, month, year)

    # Buscar todas as organizações vinculadas ao cliente (mesma lógica da view)
    organizations = db_session.query(Organization).join(
        ClientOrganization,
        Organization.id == ClientOrganization.organization_id
    ).filter(
        ClientOrganization.client_id == client_id
    ).order_by(Organization.business_name).all()

    # Buscar os módulos de ticket vinculados às aplicações contratadas pelo cliente
    allowed_ticket_modules = db_session.query(TicketModule.description).join(
        ApplicationTicketModule,
        TicketModule.id == ApplicationTicketModule.ticket_module_id
    ).join(
        ClientApplication,
        ApplicationTicketModule.application_id == ClientApplication.application_id
    ).filter(
        ClientApplication.client_id == client_id,
        ClientApplication.is_active == True
    ).distinct().all()

    # Converter para lista de strings (descrições dos módulos)
    allowed_modules_list = [module[0] for module in allowed_ticket_modules]

    # Buscar tickets para cada organização (mesma lógica da view)
    tickets_by_org = {}
    total_tickets = 0

    for org in organizations:
        tickets = ticket_service.get_tickets_by_organization(org.business_name)
        org_tickets = []

        # Filtrar tickets por período e por módulos contratados
        for ticket in tickets:
            if ticket.get('createdDate'):
                try:
                    ticket_date = datetime.fromisoformat(ticket['createdDate'])
                    # Verificar se o ticket está no período E se o módulo está na lista de contratados
                    if start_date <= ticket_date.date() <= end_date:
                        # Obter o módulo do ticket do campo customFieldModule
                        ticket_module = ticket.get('customFieldModule')

                        # Apenas incluir o ticket se o módulo estiver na lista de módulos contratados
                        if ticket_module and ticket_module in allowed_modules_list:
                            org_tickets.append({
                                'numero': ticket.get('id'),
                                'modulo': ticket.get('serviceFull', 'Não especificado'),
                                'setor': ticket.get('ownerName', 'Não atribuído')
                            })
                            total_tickets += 1
                except Exception as e:
                    continue

        if org_tickets:
            tickets_by_org[org.business_name] = org_tickets

    # Gerar número do ofício: usar customizado ou gerar automaticamente
    if oficio_number_custom:
        oficio_numero = oficio_number_custom
    else:
        oficio_numero = f"{client_id:03d}/Better Tech/{year}"

    # Gerar data por extenso em português
    meses_pt = {
        1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril',
        5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto',
        9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
    }
    hoje = datetime.now()
    data_extenso = f"{hoje.day} de {meses_pt[hoje.month]} de {hoje.year}"

    # Gerar PDF
    buffer = BytesIO()
    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2.5*cm,
        leftMargin=2.5*cm,
        topMargin=0.8*cm,
        bottomMargin=2*cm
    )

    # Estilos
    styles = getSampleStyleSheet()

    # Estilo para cabeçalho da empresa
    style_header = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=0.1*cm,
        leading=12
    )

    # Estilo para número do ofício
    style_oficio = ParagraphStyle(
        'Oficio',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica-Bold',
        textColor=colors.black,
        alignment=TA_LEFT,
        spaceAfter=0.5*cm
    )

    # Estilo para data
    style_data = ParagraphStyle(
        'Data',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_RIGHT,
        spaceAfter=0.5*cm
    )

    # Estilo para destinatário
    style_destinatario = ParagraphStyle(
        'Destinatario',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica-Bold',
        textColor=colors.black,
        alignment=TA_LEFT,
        spaceAfter=0.8*cm
    )

    # Estilo para corpo do texto
    style_body = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        alignment=TA_JUSTIFY,
        spaceAfter=0.4*cm,
        leading=16,
        firstLineIndent=0
    )

    # Estilo para seção (negrito)
    style_section = ParagraphStyle(
        'Section',
        parent=styles['Normal'],
        fontSize=12,
        fontName='Helvetica-Bold',
        textColor=colors.black,
        alignment=TA_LEFT,
        spaceAfter=0.4*cm,
        spaceBefore=0.3*cm
    )

    # Estilo para assinatura
    style_assinatura = ParagraphStyle(
        'Assinatura',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=0.1*cm
    )

    # Estilo para rodapé
    style_footer = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=7,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=0.05*cm
    )

    # Estilo para nome da organização
    style_organizacao = ParagraphStyle(
        'Organizacao',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica-Bold',
        textColor=colors.black,
        alignment=TA_LEFT,
        spaceAfter=0.4*cm,
        spaceBefore=0.3*cm,
        leftIndent=0*cm
    )

    # Estilo para item de ticket
    style_ticket = ParagraphStyle(
        'Ticket',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.black,
        alignment=TA_LEFT,
        spaceAfter=0.15*cm,
        leftIndent=0.5*cm
    )

    # Estilo para texto pequeno (total de tickets)
    style_small = ParagraphStyle(
        'Small',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.black,
        alignment=TA_LEFT,
        spaceAfter=0.4*cm
    )

    # Conteúdo
    story = []

    # LOGO DA EMPRESA CENTRALIZADA
    # Usar caminho absoluto baseado no diretório da aplicação
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    logo_path = os.path.join(base_dir, 'static', 'images', 'letterhead_logo.png')
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=6*cm, height=3*cm, kind='proportional')
        logo.hAlign = 'CENTER'
        story.append(logo)
        story.append(Spacer(1, 0.3*cm))

    # CABEÇALHO DA EMPRESA CENTRALIZADO
    story.append(Paragraph("<b>BETTER TECH INFORMÁTICA, SERVIÇOS DE AUTOMAÇÃO LTDA.</b>", style_header))
    story.append(Paragraph("Rua Leonório Perdocini, nº 1997 • Bairro Eldorado • CEP 76.966-192 • Cacoal/RO", style_header))
    story.append(Paragraph("CNPJ: 07.114.391/0001-14 • Telefone: (69) 3441-1304 • E-mail: contato@bettertech.com.br", style_header))
    story.append(Spacer(1, 0.8*cm))

    # NÚMERO DO OFÍCIO
    story.append(Paragraph(f"Ofício nº {oficio_numero}", style_oficio))

    # DATA E LOCAL
    story.append(Paragraph(f"Cacoal – RO, {data_extenso}.", style_data))
    story.append(Spacer(1, 0.3*cm))

    # DESTINATÁRIO
    story.append(Paragraph("Ao Ilmo. Sr.(a),", style_body))
    story.append(Paragraph(client['name'].upper(), style_destinatario))

    # TEXTO INTRODUTÓRIO
    # Verificar se existem informações de contrato
    contract_info = ""
    if client.get('meta'):
        contract_number = client['meta'].get('contract_number')
        contract_year = client['meta'].get('contract_year')
        process_number = client['meta'].get('process_number')
        process_year = client['meta'].get('process_year')

        if contract_number and contract_year:
            contract_info = f" de nº {contract_number}/{contract_year}"

        if process_number and process_year:
            if contract_info:
                contract_info += f", oriundo do Processo Administrativo nº {process_number}/{process_year}"
            else:
                contract_info = f", oriundo do Processo Administrativo nº {process_number}/{process_year}"

    texto_intro = f"""Prezado(a) Senhor(a),<br/><br/>

    Vimos, por meio do presente, em cumprimento às cláusulas contratuais estabelecidas no instrumento contratual{contract_info},
    apresentar o <b>Relatório Circunstanciado de Serviços Prestados</b>, referente ao período compreendido entre
    <b>{start_date.strftime('%d/%m/%Y')}</b> e <b>{end_date.strftime('%d/%m/%Y')}</b>, conforme discriminação a seguir:"""
    story.append(Paragraph(texto_intro, style_body))

    # Adicionar informações adicionais se houver nota fiscal
    if invoice_number:
        story.append(Paragraph(f"<b>Nota Fiscal:</b> {invoice_number}", style_body))

    # Buscar e listar módulos do cliente
    client_applications = client_service.get_client_applications(client_id)
    if client_applications:
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph("<b>Sistemas Contratados:</b>", style_body))

        # Dividir módulos em duas colunas
        modules_data = []
        mid_point = (len(client_applications) + 1) // 2  # Dividir ao meio, arredondando para cima

        for i in range(mid_point):
            left_module = client_applications[i]
            left_text = f"• {left_module.get('name', 'Não especificado')}"

            # Verificar se existe módulo para a coluna direita
            right_text = ""
            if i + mid_point < len(client_applications):
                right_module = client_applications[i + mid_point]
                right_text = f"• {right_module.get('name', 'Não especificado')}"

            modules_data.append([
                Paragraph(left_text, style_ticket),
                Paragraph(right_text, style_ticket) if right_text else Paragraph("", style_ticket)
            ])

        # Criar tabela com duas colunas
        modules_table = Table(modules_data, colWidths=[8*cm, 8*cm])
        modules_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(modules_table)

    story.append(Spacer(1, 0.5*cm))

    # SEÇÃO SERVIÇOS REALIZADOS
    story.append(Paragraph("<b>1. DOS SERVIÇOS EXECUTADOS</b>", style_section))
    story.append(Spacer(1, 0.3*cm))

    # Item 1.1
    texto_servico = """<b>1.1.</b> Disponibilização e manutenção de sistemas aplicativos em plataforma integrada,
    compreendendo a locação de software, suporte técnico especializado, treinamento de usuários
    e consultoria em tecnologia da informação, conforme especificações técnicas contratuais."""
    story.append(Paragraph(texto_servico, style_body))

    # Item 1.2
    story.append(Paragraph("""<b>1.2.</b> Controle de qualidade e auditoria técnica realizados pela equipe especializada
    da CONTRATADA, atestando a conformidade integral dos serviços prestados com os parâmetros estabelecidos
    no instrumento contratual vigente.""", style_body))

    # Item 1.3 - Lista de tickets agrupados por organização
    if tickets_by_org:
        texto_tickets_intro = """<b>1.3.</b> Atendimentos técnicos especializados realizados através de múltiplos canais
        de comunicação (telefone, e-mail, acesso remoto e sistema de chamados MoviDesk), conforme discriminação
        a seguir:"""
        story.append(Paragraph(texto_tickets_intro, style_body))
        story.append(Spacer(1, 0.3*cm))

        # Iterar por cada organização e seus tickets
        for org_name, tickets in tickets_by_org.items():
            # Nome da organização
            story.append(Paragraph(f"<b>• {org_name}</b>", style_organizacao))

            # Dividir tickets em duas colunas
            tickets_data = []
            mid_point = (len(tickets) + 1) // 2  # Dividir ao meio, arredondando para cima

            for i in range(mid_point):
                left_ticket = tickets[i]
                left_text = f"Ticket nº <b>{left_ticket['numero']}</b>"
                # Validar módulo
                if left_ticket['modulo'] and left_ticket['modulo'] != 'Não especificado':
                    left_text += f" - {left_ticket['modulo']}"
                else:
                    left_text += " - Outros Assuntos"

                # Verificar se existe ticket para a coluna direita
                right_text = ""
                if i + mid_point < len(tickets):
                    right_ticket = tickets[i + mid_point]
                    right_text = f"Ticket nº <b>{right_ticket['numero']}</b>"
                    # Validar módulo
                    if right_ticket['modulo'] and right_ticket['modulo'] != 'Não especificado':
                        right_text += f" - {right_ticket['modulo']}"
                    else:
                        right_text += " - Outros Assuntos"

                tickets_data.append([
                    Paragraph(left_text, style_ticket),
                    Paragraph(right_text, style_ticket) if right_text else Paragraph("", style_ticket)
                ])

            # Criar tabela com duas colunas
            tickets_table = Table(tickets_data, colWidths=[8*cm, 8*cm])
            tickets_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ]))
            story.append(tickets_table)
            story.append(Spacer(1, 0.3*cm))

        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph(f"Total de atendimentos registrados no período: <b>{total_tickets}</b> ticket(s).", style_small))
        story.append(Spacer(1, 0.5*cm))
    else:
        story.append(Paragraph("""<b>1.3.</b> Não foram registrados atendimentos técnicos através do sistema de chamados
        MoviDesk durante o período de referência, evidenciando a estabilidade operacional dos sistemas
        sob gestão da CONTRATADA.""", style_body))

    # Item 1.4
    story.append(Paragraph("""<b>1.4.</b> Gestão de credenciais de acesso e controles de segurança dos sistemas
    aplicativos, incluindo liberação, revogação e renovação de senhas, em conformidade com as políticas
    de segurança da informação estabelecidas.""", style_body))

    story.append(Spacer(1, 0.5*cm))

    # SEÇÃO CONCLUSÃO
    story.append(Paragraph("<b>2. DAS CONSIDERAÇÕES FINAIS</b>", style_section))
    story.append(Spacer(1, 0.3*cm))

    texto_conclusao = """Atestamos que todos os serviços foram executados em conformidade com as especificações
    técnicas e cláusulas contratuais estabelecidas, com observância aos padrões de qualidade e prazos acordados.
    A CONTRATADA mantém-se à disposição para quaisquer esclarecimentos adicionais que se façam necessários."""
    story.append(Paragraph(texto_conclusao, style_body))

    story.append(Spacer(1, 1.5*cm))

    # ENCERRAMENTO
    story.append(Paragraph("Na oportunidade, renovamos nossos votos de elevada estima e consideração.", style_body))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Atenciosamente,", style_body))
    story.append(Spacer(1, 0.5*cm))

    # ASSINATURA - IMAGEM
    signature_path = os.path.join(base_dir, 'static', 'images', 'signature_ronildo_pauli.png')
    if os.path.exists(signature_path):
        signature = Image(signature_path, width=6*cm, height=3*cm, kind='proportional')
        signature.hAlign = 'CENTER'
        story.append(signature)
    else:
        # Fallback caso a assinatura não exista
        story.append(Spacer(1, 2*cm))
        story.append(Paragraph("_______________________________", style_assinatura))

    story.append(Paragraph("<b>Better Tech Informática, Serviços de Automação LTDA.</b>", style_assinatura))
    story.append(Paragraph("CNPJ: 07.114.391/0001-14", style_assinatura))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Ronildo Pauli", style_assinatura))
    story.append(Paragraph("Sócio Administrador", style_assinatura))

    # Gerar PDF com rodapé automático em todas as páginas
    pdf.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)

    # Preparar resposta
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'

    # Verificar se deve forçar download ou visualizar
    download = request.args.get('download', '0')
    filename = f'relatorio_servico_{client["name"].replace(" ", "_")}_{month:02d}_{year}.pdf'

    if download == '1':
        # Forçar download
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    else:
        # Visualizar inline no navegador
        response.headers['Content-Disposition'] = f'inline; filename={filename}'

    return response


def calculate_billing_period(client, month, year):
    """Calcula período de cobrança baseado no ciclo do cliente"""
    billing_cycle_type = client.get('billing_cycle_type')

    if billing_cycle_type == 'mensal':
        # Ciclo Mensal: sempre do dia 1 até o último dia do mês
        start_date = datetime(year, month, 1).date()

        # Próximo mês para calcular o último dia do mês atual
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1
        end_date = datetime(next_year, next_month, 1).date() - timedelta(days=1)

    elif billing_cycle_type == 'fixo':
        # Ciclo Fixo: do dia fixo até o mesmo dia do mês seguinte
        start_day = client.get('fixed_start_day', 1)
        start_date = datetime(year, month, start_day).date()

        # Próximo mês, mesmo dia
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1

        try:
            end_date = datetime(next_year, next_month, start_day).date()
        except ValueError:
            # Se o dia não existir no próximo mês (ex: 31 em fevereiro), usar último dia do mês
            end_date = datetime(next_year, next_month, 1).date() - timedelta(days=1)

    else:
        # Sem ciclo definido: mês completo
        start_date = datetime(year, month, 1).date()
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1
        end_date = datetime(next_year, next_month, 1).date() - timedelta(days=1)

    return start_date, end_date


def get_billing_cycle_text(client):
    """Retorna texto descritivo do ciclo de cobrança"""
    billing_cycle_type = client.get('billing_cycle_type')

    if billing_cycle_type == 'mensal':
        return "Mensal (dia 1 ao último dia do mês)"
    elif billing_cycle_type == 'fixo':
        fixed_start_day = client.get('fixed_start_day', 1)
        return f"Fixo (dia {fixed_start_day} ao dia {fixed_start_day} do mês seguinte)"
    else:
        return "Não definido"
