from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from stock.models import Alerte
from stock.decorators import role_required


@login_required
def liste(request):
    is_read = request.GET.get('is_read', '')
    alertes = Alerte.objects.select_related('produit').all()
    
    if is_read == 'true':
        alertes = alertes.filter(is_read=True)
    elif is_read == 'false':
        alertes = alertes.filter(is_read=False)
    
    return render(request, 'stock/alertes/liste.html', {
        'alertes': alertes,
        'is_read': is_read,
    })


@login_required
def marquer_lu(request, pk):
    alerte = Alerte.objects.get(pk=pk)
    alerte.is_read = True
    alerte.save()
    messages.info(request, 'Alerte marquée comme lue.')
    return redirect('alertes_liste')


@login_required
@role_required('admin', 'gestionnaire')
def marquer_tous_lus(request):
    Alerte.objects.filter(is_read=False).update(is_read=True)
    messages.success(request, 'Toutes les alertes ont été marquées comme lues.')
    return redirect('alertes_liste')
