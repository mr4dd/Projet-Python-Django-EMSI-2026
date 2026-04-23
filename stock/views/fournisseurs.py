from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from stock.models import Fournisseur
from stock.forms import FournisseurForm
from stock.decorators import role_required


@login_required
def liste(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'stock/fournisseurs/liste.html', {
        'fournisseurs': fournisseurs,
    })


@login_required
@role_required('admin', 'gestionnaire')
def ajouter(request):
    form = FournisseurForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Fournisseur ajouté!')
        return redirect('fournisseurs_liste')
    return render(request, 'stock/fournisseurs/form.html', {
        'form': form,
        'titre': 'Ajouter un fournisseur'
    })


@login_required
@role_required('admin', 'gestionnaire')
def modifier(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    form = FournisseurForm(request.POST or None, instance=fournisseur)
    if form.is_valid():
        form.save()
        messages.success(request, 'Fournisseur modifié!')
        return redirect('fournisseurs_liste')
    return render(request, 'stock/fournisseurs/form.html', {
        'form': form,
        'titre': 'Modifier un fournisseur',
        'fournisseur': fournisseur
    })


@login_required
@role_required('admin')
def supprimer(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    if request.method == 'POST':
        nom = fournisseur.nom
        fournisseur.delete()
        messages.success(request, f'Fournisseur "{nom}" supprimé!')
        return redirect('fournisseurs_liste')
    return render(request, 'stock/fournisseurs/confirmer_suppression.html', {
        'fournisseur': fournisseur
    })
