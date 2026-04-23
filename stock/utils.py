from .models import Alerte


def check_and_create_alerte(produit):
    if produit.quantite_stock <= produit.seuil_alerte:
        if not Alerte.objects.filter(produit=produit, is_read=False).exists():
            Alerte.objects.create(
                produit=produit,
                message=(
                    f"Stock bas : {produit.nom} — "
                    f"{produit.quantite_stock} unité(s) restante(s) "
                    f"(seuil : {produit.seuil_alerte})"
                )
            )


def quantite_suggere(produit):
    return produit.seuil_alerte * 2


def generer_rapport_inventaire():
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm
    from django.http import HttpResponse
    from .models import Produit
    from datetime import datetime

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="inventaire.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Rapport d'inventaire", styles['Title']))
    elements.append(Paragraph(f"Généré le : {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 0.5 * cm))

    data = [['Référence', 'Produit', 'Catégorie', 'Fournisseur', 'Qté', 'Prix unit.', 'Valeur']]
    produits = Produit.objects.select_related('categorie', 'fournisseur').all()
    total_valeur = 0

    for p in produits:
        valeur = p.valeur_stock()
        total_valeur += valeur
        data.append([
            p.reference, p.nom, p.categorie.nom, p.fournisseur.nom,
            str(p.quantite_stock), f"{p.prix:.2f} MAD", f"{valeur:.2f} MAD"
        ])

    data.append(['', '', '', '', '', 'TOTAL', f"{total_valeur:.2f} MAD"])

    table = Table(data, colWidths=[2.5*cm, 4*cm, 3*cm, 3*cm, 1.5*cm, 2.5*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a3c5e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f0f4f8')]),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f0fe')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    elements.append(table)
    doc.build(elements)
    return response
