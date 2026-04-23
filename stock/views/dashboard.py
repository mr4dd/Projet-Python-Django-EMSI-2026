from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from stock.models import Produit, MouvementStock, Alerte, BonCommande
from django.db.models import Sum, Count, F
from django.utils import timezone
import json
from datetime import timedelta


@login_required
def index(request):
    # Summary stats
    total_produits = Produit.objects.count()
    valeur_stock = sum(p.valeur_stock() for p in Produit.objects.all())
    produits_bas = Produit.objects.filter(quantite_stock__lte=F('seuil_alerte')).count()
    alertes_ouvertes = Alerte.objects.filter(is_read=False).count()
    commandes_en_cours = BonCommande.objects.exclude(statut__in=['recu', 'annule']).count()

    # Chart: last 7 days movements
    labels = []
    entrees_data = []
    sorties_data = []
    for i in range(6, -1, -1):
        day = timezone.now().date() - timedelta(days=i)
        labels.append(day.strftime('%d/%m'))
        entrees_data.append(
            MouvementStock.objects.filter(type_mouvement='entree', date__date=day)
            .aggregate(total=Sum('quantite'))['total'] or 0
        )
        sorties_data.append(
            MouvementStock.objects.filter(type_mouvement='sortie', date__date=day)
            .aggregate(total=Sum('quantite'))['total'] or 0
        )

    context = {
        'total_produits': total_produits,
        'valeur_stock': f"{valeur_stock:.2f}",
        'produits_bas': produits_bas,
        'alertes_ouvertes': alertes_ouvertes,
        'commandes_en_cours': commandes_en_cours,
        'chart_labels': json.dumps(labels),
        'chart_entrees': json.dumps(entrees_data),
        'chart_sorties': json.dumps(sorties_data),
    }
    return render(request, 'stock/dashboard.html', context)
