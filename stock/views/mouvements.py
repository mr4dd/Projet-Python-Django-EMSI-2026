from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from stock.models import MouvementStock
from stock.forms import MouvementStockForm
from stock.decorators import role_required


@login_required
def liste(request):
    mouvements = MouvementStock.objects.select_related('produit', 'utilisateur').all()
    
    # Filter
    produit = request.GET.get('produit', '')
    type_mouvement = request.GET.get('type', '')
    
    if produit:
        mouvements = mouvements.filter(produit__id=produit)
    
    if type_mouvement:
        mouvements = mouvements.filter(type_mouvement=type_mouvement)
    
    from stock.models import Produit
    produits = Produit.objects.all()
    
    return render(request, 'stock/mouvements/liste.html', {
        'mouvements': mouvements,
        'produits': produits,
        'produit': produit,
        'type_mouvement': type_mouvement,
    })


@login_required
@role_required('admin', 'gestionnaire')
def ajouter(request):
    form = MouvementStockForm(request.POST or None)
    if form.is_valid():
        mouvement = form.save(commit=False)
        mouvement.utilisateur = request.user
        mouvement.save()
        messages.success(request, 'Mouvement de stock enregistré!')
        return redirect('mouvements_liste')
    return render(request, 'stock/mouvements/form.html', {
        'form': form,
        'titre': 'Enregistrer un mouvement de stock'
    })
