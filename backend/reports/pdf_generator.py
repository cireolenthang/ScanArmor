from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(scan_result, out_path):
    """Generates a professional security PDF report using ReportLab."""
    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )
    story = []
    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=12
    )
    
    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#475569")
    )

    header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        textColor=colors.white
    )

    # 1. Report Header
    story.append(Paragraph("<b>SMB SHIELD SECURITY REPORT</b>", title_style))
    story.append(Spacer(1, 10))

    # 2. Executive Summary Table
    target = scan_result.get('target', 'N/A')
    score = str(scan_result.get('score', 'N/A'))
    grade = scan_result.get('grade', 'N/A')

    summary_data = [
        [Paragraph("<b>Target Domain:</b>", meta_style), Paragraph(target, meta_style)],
        [Paragraph("<b>Security Score:</b>", meta_style), Paragraph(f"<b>{score} / 100</b>", meta_style)],
        [Paragraph("<b>Overall Grade:</b>", meta_style), Paragraph(f"<b>{grade}</b>", meta_style)],
    ]
    
    summary_table = Table(summary_data, colWidths=[120, 420])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))

    # 3. Detailed Security Findings Table
    story.append(Paragraph("<b>Identified Vulnerabilities & Issues</b>", styles['Heading2']))
    story.append(Spacer(1, 10))

    issues = scan_result.get('issues', [])
    if not issues:
        story.append(Paragraph("No security issues detected.", meta_style))
    else:
        issues_table_data = [[
            Paragraph("<b>Severity</b>", header_style),
            Paragraph("<b>Check</b>", header_style),
            Paragraph("<b>Issue Title & Details</b>", header_style)
        ]]
        
        # Color mapping for severity badges
        severity_colors = {
            "critical": colors.HexColor("#ef4444"),
            "high": colors.HexColor("#f97316"),
            "medium": colors.HexColor("#eab308"),
            "low": colors.HexColor("#3b82f6"),
            "info": colors.HexColor("#64748b")
        }

        for issue in issues:
            sev = str(issue.get('severity', 'info')).lower()
            title = issue.get('title', '')
            detail = issue.get('detail', '')
            check = issue.get('check', 'N/A')

            sev_p = Paragraph(f"<font color='white'><b>{sev.upper()}</b></font>", ParagraphStyle('Sev', alignment=1))
            check_p = Paragraph(f"<b>{check}</b>", meta_style)
            detail_p = Paragraph(f"<b>{title}</b><br/><font color='#64748b'>{detail}</font>", meta_style)

            issues_table_data.append([sev_p, check_p, detail_p])

        issues_table = Table(issues_table_data, colWidths=[80, 80, 380])
        
        t_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]

        # Apply background colors to Severity badges dynamically
        for idx, issue in enumerate(issues, start=1):
            sev = str(issue.get('severity', 'info')).lower()
            bg_color = severity_colors.get(sev, colors.HexColor("#64748b"))
            t_style.append(('BACKGROUND', (0, idx), (0, idx), bg_color))

        issues_table.setStyle(TableStyle(t_style))
        story.append(issues_table)

    # Build document
    doc.build(story)