from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from stock.models import MouvementStock, Produit
from stock.decorators import role_required
from stock.utils import generer_rapport_inventaire
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from datetime import datetime, timedelta
from django.utils import timezone


@login_required
@role_required('admin', 'gestionnaire')
def inventaire_pdf(request):
    return generer_rapport_inventaire()


@login_required
@role_required('admin', 'gestionnaire')
def mouvements_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mouvements.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Rapport des mouvements de stock", styles['Title']))
    elements.append(Paragraph(f"Généré le : {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 0.5 * cm))

    date_limite = timezone.now() - timedelta(days=30)
    mouvements = MouvementStock.objects.filter(date__gte=date_limite).select_related(
        'produit', 'utilisateur'
    ).order_by('-date')

    data = [['Date', 'Type', 'Produit', 'Quantité', 'Utilisateur', 'Motif']]

    for m in mouvements:
        data.append([
            m.date.strftime('%d/%m/%Y %H:%M'),
            dict(MouvementStock.TYPE_CHOICES).get(m.type_mouvement, m.type_mouvement),
            m.produit.nom,
            str(m.quantite),
            m.utilisateur.get_full_name(),
            m.motif or '-',
        ])

    table = Table(data, colWidths=[2.2*cm, 2*cm, 4*cm, 1.8*cm, 3.5*cm, 4*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a3c5e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4f8')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(table)
    doc.build(elements)
    return response
