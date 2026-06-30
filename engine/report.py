from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
import datetime

def generate_report(data):
    output_path = os.path.join('static', 'reports')
    os.makedirs(output_path, exist_ok=True)
    filename = os.path.join(output_path, 'claritygrc_report.pdf')

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # COLORS — dark theme palette
    accent = colors.HexColor('#7C5CFC')
    accent_dark = colors.HexColor('#6A4AE8')
    ink = colors.HexColor('#1A1A2E')
    surface = colors.HexColor('#F8F8FC')
    text = colors.HexColor('#1A1A2E')
    text_muted = colors.HexColor('#6B6B8A')
    border = colors.HexColor('#E0E0F0')
    red = colors.HexColor('#FF4D6A')
    orange = colors.HexColor('#FF8C42')
    yellow = colors.HexColor('#FFD166')
    green = colors.HexColor('#06D6A0')
    light_gray = colors.HexColor('#F4F4F8')
    dark_gray = colors.HexColor('#2A2A3A')

    risk_colors = {
        'CRITICAL': red, 'HIGH': orange, 'MEDIUM': yellow, 'LOW': green,
        'HIGH RISK': orange, 'MINIMAL RISK': green, 'LIMITED RISK': yellow,
        'UNACCEPTABLE RISK': red, 'ESSENTIAL ENTITY': red, 'IMPORTANT ENTITY': orange,
        'FULL REGIME': red, 'SIMPLIFIED REGIME': yellow, 'NOT APPLICABLE': green,
        'LIKELY EXEMPT': green
    }

    title_style = ParagraphStyle('Title', fontSize=26, textColor=ink,
        fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=4)
    subtitle_style = ParagraphStyle('Subtitle', fontSize=10, textColor=text_muted,
        fontName='Helvetica', alignment=TA_CENTER, spaceAfter=8)
    heading_style = ParagraphStyle('Heading', fontSize=12, textColor=ink,
        fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=6)
    body_style = ParagraphStyle('Body', fontSize=9.5, textColor=dark_gray,
        fontName='Helvetica', spaceAfter=5, leading=14)
    small_style = ParagraphStyle('Small', fontSize=8, textColor=text_muted,
        fontName='Helvetica', alignment=TA_CENTER, spaceAfter=4)

    elements = []

    # HEADER
    elements.append(Spacer(1, 0.8*cm))
    elements.append(Paragraph("ClarityGRC", title_style))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph("AI Governance &amp; Compliance Assessment Report", subtitle_style))
    elements.append(Spacer(1, 0.4*cm))
    elements.append(HRFlowable(width="100%", thickness=2, color=accent))
    elements.append(Spacer(1, 0.5*cm))

    date_str = datetime.datetime.now().strftime("%B %d, %Y")
    elements.append(Paragraph(f"Assessment Date: {date_str}", small_style))
    elements.append(Paragraph(f"System Type: {data.get('system_type', 'N/A').replace('_', ' ').title()}", small_style))
    if data.get('description'):
        elements.append(Paragraph(f"Description: {data.get('description')}", small_style))
    elements.append(Spacer(1, 0.5*cm))

    # SUMMARY TABLE
    eu_class = data.get('eu_classification', 'N/A')
    risk_level = data.get('risk_level', 'N/A')
    risk_score = data.get('risk_score', 'N/A')
    dpia = 'Yes' if data.get('dpia_required') else 'No'

    eu_color = risk_colors.get(eu_class, colors.gray)
    risk_color = risk_colors.get(risk_level, colors.gray)

    summary_data = [
        ['EU AI Act', 'Risk Level', 'Risk Score', 'DPIA Required'],
        [eu_class, risk_level, f"{risk_score}/100", dpia]
    ]
    summary_table = Table(summary_data, colWidths=[4.5*cm, 3.5*cm, 3.5*cm, 3.5*cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), accent),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [light_gray]),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,1), (-1,-1), 10),
        ('TEXTCOLOR', (0,1), (0,1), eu_color),
        ('TEXTCOLOR', (1,1), (1,1), risk_color),
        ('GRID', (0,0), (-1,-1), 0.5, border),
        ('ROWHEIGHT', (0,0), (-1,-1), 0.8*cm),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.5*cm))

    # EU AI ACT
    elements.append(HRFlowable(width="100%", thickness=1, color=border))
    elements.append(Paragraph("EU AI Act Classification", heading_style))
    elements.append(Paragraph(data.get('eu_meaning', ''), body_style))
    if data.get('eu_obligations'):
        for ob in data['eu_obligations']:
            elements.append(Paragraph(f"• {ob}", body_style))
    elements.append(Spacer(1, 0.3*cm))

    # GDPR
    elements.append(HRFlowable(width="100%", thickness=1, color=border))
    elements.append(Paragraph("GDPR Obligations", heading_style))
    if data.get('gdpr_obligations'):
        for ob in data['gdpr_obligations']:
            elements.append(Paragraph(f"• {ob}", body_style))
    if data.get('gdpr_articles'):
        articles_text = "  |  ".join(data['gdpr_articles'])
        elements.append(Paragraph(f"Relevant Articles: {articles_text}", small_style))
    elements.append(Spacer(1, 0.3*cm))

    # RISK SCORE
    elements.append(HRFlowable(width="100%", thickness=1, color=border))
    elements.append(Paragraph("Risk Assessment", heading_style))
    elements.append(Paragraph(data.get('risk_advice', ''), body_style))
    if data.get('risk_breakdown'):
        for item in data['risk_breakdown']:
            elements.append(Paragraph(f"  {item}", body_style))
    elements.append(Spacer(1, 0.3*cm))

    # ISO 27001
    elements.append(HRFlowable(width="100%", thickness=1, color=border))
    elements.append(Paragraph("ISO 27001 Recommended Controls", heading_style))
    if data.get('iso_controls'):
        iso_data = [['Control', 'Name', 'Priority']]
        for control in data['iso_controls']:
            iso_data.append([control.get('id',''), control.get('name',''), control.get('priority','')])
        iso_table = Table(iso_data, colWidths=[2*cm, 10*cm, 3*cm])
        iso_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), accent),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 9),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 9),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_gray]),
            ('GRID', (0,0), (-1,-1), 0.5, border),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(iso_table)
    elements.append(Spacer(1, 0.3*cm))

    # NIS2
    elements.append(HRFlowable(width="100%", thickness=1, color=border))
    elements.append(Paragraph("NIS2 Directive", heading_style))
    if data.get('nis2_classification'):
        elements.append(Paragraph(f"Classification: {data.get('nis2_classification')}", body_style))
        elements.append(Paragraph(data.get('nis2_meaning', ''), body_style))
        if data.get('nis2_sector_note'):
            elements.append(Paragraph(f"Sector Note: {data.get('nis2_sector_note')}", body_style))
        if data.get('nis2_obligations'):
            for ob in data['nis2_obligations']:
                elements.append(Paragraph(f"• {ob}", body_style))
        if data.get('nis2_penalties'):
            elements.append(Paragraph(f"Penalties: {data.get('nis2_penalties')}", body_style))
    elements.append(Spacer(1, 0.3*cm))

    # DORA
    elements.append(HRFlowable(width="100%", thickness=1, color=border))
    elements.append(Paragraph("DORA — Digital Operational Resilience Act", heading_style))
    if data.get('dora_classification'):
        elements.append(Paragraph(f"Classification: {data.get('dora_classification')}", body_style))
        elements.append(Paragraph(data.get('dora_meaning', ''), body_style))
        if data.get('dora_obligations'):
            for ob in data['dora_obligations']:
                elements.append(Paragraph(f"• {ob}", body_style))
        if data.get('dora_penalties'):
            elements.append(Paragraph(f"Penalties: {data.get('dora_penalties')}", body_style))
    elements.append(Spacer(1, 0.3*cm))

    # ISO 42001
    elements.append(HRFlowable(width="100%", thickness=1, color=border))
    elements.append(Paragraph("ISO 42001 — AI Management System", heading_style))
    if data.get('iso42001_controls'):
        elements.append(Paragraph(data.get('iso42001_meaning', ''), body_style))
        iso42_data = [['Control', 'Name', 'Priority']]
        for control in data['iso42001_controls']:
            iso42_data.append([control.get('id',''), control.get('name',''), control.get('priority','')])
        iso42_table = Table(iso42_data, colWidths=[2*cm, 10*cm, 3*cm])
        iso42_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), accent),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 9),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 9),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_gray]),
            ('GRID', (0,0), (-1,-1), 0.5, border),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(iso42_table)
    elements.append(Spacer(1, 0.3*cm))

    # AI EXPLANATION
    if data.get('explanation'):
        elements.append(HRFlowable(width="100%", thickness=1, color=border))
        elements.append(Paragraph("AI Governance Consultant Summary", heading_style))
        elements.append(Paragraph(data.get('explanation'), body_style))
        elements.append(Spacer(1, 0.3*cm))

    # DISCLAIMER
    elements.append(HRFlowable(width="100%", thickness=1, color=border))
    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph(
        "Disclaimer: This report was generated automatically by ClarityGRC for educational and awareness purposes. "
        "It does not constitute legal advice. Please consult a qualified GRC professional or legal counsel for "
        "formal compliance assessments.",
        small_style
    ))

    doc.build(elements)
    return filename