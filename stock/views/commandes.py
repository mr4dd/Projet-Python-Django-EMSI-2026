from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import formset_factory
from stock.models import BonCommande, LigneCommande
from stock.forms import BonCommandeForm, LigneCommandeForm, BonCommandeStatusForm
from stock.decorators import role_required


@login_required
def liste(request):
    bons = BonCommande.objects.select_related('fournisseur', 'cree_par').all()
    
    # Filter by status
    statut = request.GET.get('statut', '')
    if statut:
        bons = bons.filter(statut=statut)
    
    return render(request, 'stock/commandes/liste.html', {
        'bons': bons,
        'statut': statut,
    })


@login_required
@role_required('admin', 'gestionnaire')
def creer(request):
    form = BonCommandeForm(request.POST or None)
    if form.is_valid():
        bon = form.save(commit=False)
        bon.cree_par = request.user
        bon.save()
        messages.success(request, 'Bon de commande créé!')
        return redirect('commandes_detail', pk=bon.pk)
    return render(request, 'stock/commandes/form.html', {
        'form': form,
        'titre': 'Créer un bon de commande'
    })


@login_required
def detail(request, pk):
    bon = get_object_or_404(BonCommande, pk=pk)
    lignes = bon.lignes.select_related('produit').all()
    
    status_form = BonCommandeStatusForm(request.POST or None, instance=bon)
    if request.method == 'POST' and 'status' in request.POST and status_form.is_valid():
        status_form.save()
        messages.success(request, 'Statut mis à jour!')
        return redirect('commandes_detail', pk=bon.pk)
    
    return render(request, 'stock/commandes/detail.html', {
        'bon': bon,
        'lignes': lignes,
        'status_form': status_form,
    })


@login_required
@role_required('admin', 'gestionnaire')
def ajouter_ligne(request, pk):
    bon = get_object_or_404(BonCommande, pk=pk)
    form = LigneCommandeForm(request.POST or None)
    if form.is_valid():
        ligne = form.save(commit=False)
        ligne.bon_commande = bon
        ligne.save()
        messages.success(request, 'Ligne de commande ajoutée!')
        return redirect('commandes_detail', pk=bon.pk)
    return render(request, 'stock/commandes/ajouter_ligne.html', {
        'form': form,
        'bon': bon
    })


@login_required
@role_required('admin', 'gestionnaire')
def supprimer_ligne(request, pk, ligne_id):
    bon = get_object_or_404(BonCommande, pk=pk)
    ligne = get_object_or_404(LigneCommande, pk=ligne_id, bon_commande=bon)
    
    if request.method == 'POST':
        ligne.delete()
        messages.success(request, 'Ligne de commande supprimée!')
        return redirect('commandes_detail', pk=bon.pk)
    
    return render(request, 'stock/commandes/confirmer_suppression_ligne.html', {
        'bon': bon,
        'ligne': ligne
    })
