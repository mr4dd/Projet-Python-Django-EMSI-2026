from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from stock.models import Produit, Categorie
from stock.forms import ProduitForm
from stock.decorators import role_required


@login_required
def liste(request):
    produits = Produit.objects.select_related('categorie', 'fournisseur').all()
    
    # Search and filter
    search = request.GET.get('search', '')
    categorie = request.GET.get('categorie', '')
    
    if search:
        produits = produits.filter(Q(nom__icontains=search) | Q(reference__icontains=search))
    
    if categorie:
        produits = produits.filter(categorie__id=categorie)
    
    categories = Categorie.objects.all()
    
    return render(request, 'stock/produits/liste.html', {
        'produits': produits,
        'categories': categories,
        'search': search,
        'categorie': categorie,
    })


@login_required
@role_required('admin', 'gestionnaire')
def ajouter(request):
    form = ProduitForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Produit ajouté avec succès!')
        return redirect('produits_liste')
    return render(request, 'stock/produits/form.html', {
        'form': form,
        'titre': 'Ajouter un produit'
    })


@login_required
@role_required('admin', 'gestionnaire')
def modifier(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    form = ProduitForm(request.POST or None, instance=produit)
    if form.is_valid():
        form.save()
        messages.success(request, 'Produit modifié avec succès!')
        return redirect('produits_liste')
    return render(request, 'stock/produits/form.html', {
        'form': form,
        'titre': 'Modifier le produit',
        'produit': produit
    })


@login_required
@role_required('admin')
def supprimer(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        nom = produit.nom
        produit.delete()
        messages.success(request, f'Produit "{nom}" supprimé avec succès!')
        return redirect('produits_liste')
    return render(request, 'stock/produits/confirmer_suppression.html', {'produit': produit})


@login_required
def detail(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    mouvements = produit.mouvements.all()[:10]
    alertes = produit.alertes.all()[:5]
    
    return render(request, 'stock/produits/detail.html', {
        'produit': produit,
        'mouvements': mouvements,
        'alertes': alertes,
    })
