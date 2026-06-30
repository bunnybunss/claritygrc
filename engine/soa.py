import os
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def generate_soa(data):
    output_path = os.path.join('static', 'reports')
    os.makedirs(output_path, exist_ok=True)
    filename = os.path.join(output_path, 'claritygrc_soa.pdf')

    doc = SimpleDocTemplate(
        filename, pagesize=A4,
        rightMargin=1.5*cm, leftMargin=1.5*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )

    accent = colors.HexColor('#7C5CFC')
    ink = colors.HexColor('#1A1A2E')
    text_muted = colors.HexColor('#6B6B8A')
    border = colors.HexColor('#E0E0F0')
    light_gray = colors.HexColor('#F4F4F8')
    dark_gray = colors.HexColor('#2A2A3A')

    title_style = ParagraphStyle('Title', fontSize=22, textColor=ink,
        fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=4)
    subtitle_style = ParagraphStyle('Subtitle', fontSize=10, textColor=text_muted,
        fontName='Helvetica', alignment=TA_CENTER, spaceAfter=8)
    small_style = ParagraphStyle('Small', fontSize=8, textColor=text_muted,
        fontName='Helvetica', alignment=TA_CENTER, spaceAfter=4)
    heading_style = ParagraphStyle('Heading', fontSize=11, textColor=ink,
        fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=6)
    body_style = ParagraphStyle('Body', fontSize=8, textColor=dark_gray,
        fontName='Helvetica', spaceAfter=2, leading=11)

    priority_justifications = {
        'Critical': 'Mandatory — critical risk identified',
        'High': 'Required — high risk exposure',
        'Medium': 'Recommended — best practice'
    }

    elements = []

    # HEADER
    elements.append(Spacer(1, 0.8*cm))
    elements.append(Paragraph("ClarityGRC", title_style))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph("Statement of Applicability", subtitle_style))
    elements.append(Spacer(1, 0.4*cm))
    elements.append(HRFlowable(width="100%", thickness=2, color=accent))
    elements.append(Spacer(1, 0.5*cm))

    system_name = data.get('system_name', 'Unknown System')
    system_type = data.get('system_type', 'N/A').replace('_', ' ').title()
    date_str = datetime.datetime.now().strftime("%B %d, %Y")

    elements.append(Paragraph(f"Organization / System: {system_name}", small_style))
    elements.append(Paragraph(f"System Type: {system_type}", small_style))
    elements.append(Paragraph(f"Document Date: {date_str}", small_style))
    elements.append(Paragraph(f"EU AI Act Classification: {data.get('eu_classification', 'N/A')}", small_style))
    elements.append(Paragraph(f"Overall Risk Score: {data.get('risk_score', 'N/A')}/100 — {data.get('risk_level', 'N/A')}", small_style))
    elements.append(Spacer(1, 0.5*cm))

    # ISO 27001 TABLE
    elements.append(HRFlowable(width="100%", thickness=1, color=border))
    elements.append(Paragraph("ISO 27001 — Statement of Applicability", heading_style))
    elements.append(Paragraph(
        "The following table identifies ISO 27001 controls applicable to this system, "
        "their current implementation status, and assigned ownership.",
        body_style
    ))
    elements.append(Spacer(1, 0.3*cm))

    iso_headers = [
        Paragraph('<b>Control</b>', body_style),
        Paragraph('<b>Name</b>', body_style),
        Paragraph('<b>Applicable</b>', body_style),
        Paragraph('<b>Status</b>', body_style),
        Paragraph('<b>Justification</b>', body_style),
        Paragraph('<b>Owner</b>', body_style)
    ]
    iso_rows = [iso_headers]

    for control in data.get('iso_controls', []):
        justification = priority_justifications.get(control.get('priority', ''), 'Required')
        iso_rows.append([
            Paragraph(control.get('id', ''), body_style),
            Paragraph(control.get('name', ''), body_style),
            Paragraph('Yes', body_style),
            Paragraph('Not Started', body_style),
            Paragraph(justification, body_style),
            Paragraph('To be assigned', body_style)
        ])

    iso_table = Table(iso_rows, colWidths=[1.5*cm, 4.5*cm, 1.8*cm, 2.2*cm, 4.5*cm, 2.7*cm])
    iso_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), accent),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_gray]),
        ('GRID', (0,0), (-1,-1), 0.3, border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(iso_table)
    elements.append(Spacer(1, 0.6*cm))

    # ISO 42001 TABLE
    elements.append(HRFlowable(width="100%", thickness=1, color=border))
    elements.append(Paragraph("ISO 42001 — AI Management System Controls", heading_style))
    elements.append(Paragraph(
        "ISO 42001 AI management system controls applicable to this system, "
        "directly aligned with EU AI Act compliance requirements.",
        body_style
    ))
    elements.append(Spacer(1, 0.3*cm))

    iso42_headers = [
        Paragraph('<b>Control</b>', body_style),
        Paragraph('<b>Name</b>', body_style),
        Paragraph('<b>Applicable</b>', body_style),
        Paragraph('<b>Status</b>', body_style),
        Paragraph('<b>Priority</b>', body_style),
        Paragraph('<b>Owner</b>', body_style)
    ]
    iso42_rows = [iso42_headers]

    for control in data.get('iso42001_controls', []):
        iso42_rows.append([
            Paragraph(control.get('id', ''), body_style),
            Paragraph(control.get('name', ''), body_style),
            Paragraph('Yes', body_style),
            Paragraph('Not Started', body_style),
            Paragraph(control.get('priority', ''), body_style),
            Paragraph('To be assigned', body_style)
        ])

    iso42_table = Table(iso42_rows, colWidths=[1.5*cm, 5*cm, 1.8*cm, 2.2*cm, 2.2*cm, 2.5*cm])
    iso42_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), accent),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_gray]),
        ('GRID', (0,0), (-1,-1), 0.3, border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(iso42_table)
    elements.append(Spacer(1, 0.6*cm))

    # GDPR TABLE
    elements.append(HRFlowable(width="100%", thickness=1, color=border))
    elements.append(Paragraph("GDPR — Data Protection Obligations", heading_style))
    elements.append(Spacer(1, 0.2*cm))

    gdpr_headers = [
        Paragraph('<b>Obligation</b>', body_style),
        Paragraph('<b>Status</b>', body_style),
        Paragraph('<b>Owner</b>', body_style),
        Paragraph('<b>Notes</b>', body_style)
    ]
    gdpr_rows = [gdpr_headers]

    for ob in data.get('gdpr_obligations', []):
        gdpr_rows.append([
            Paragraph(ob, body_style),
            Paragraph('Not Started', body_style),
            Paragraph('To be assigned', body_style),
            Paragraph('', body_style)
        ])

    gdpr_table = Table(gdpr_rows, colWidths=[7*cm, 2.5*cm, 3.2*cm, 4.5*cm])
    gdpr_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), accent),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_gray]),
        ('GRID', (0,0), (-1,-1), 0.3, border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(gdpr_table)
    elements.append(Spacer(1, 0.6*cm))

    # DISCLAIMER
    elements.append(HRFlowable(width="100%", thickness=1, color=border))
    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph(
        "This Statement of Applicability was generated automatically by ClarityGRC. "
        "It is intended as a starting point for your compliance programme. "
        "Status and ownership fields should be completed by your compliance team. "
        "This document does not constitute legal advice.",
        small_style
    ))

    doc.build(elements)
    return filename