from django.urls import path
from stock.views import dashboard, produits, mouvements, commandes, fournisseurs, alertes, rapports

urlpatterns = [
    path('dashboard/', dashboard.index, name='dashboard'),

    path('produits/', produits.liste, name='produits_liste'),
    path('produits/ajouter/', produits.ajouter, name='produits_ajouter'),
    path('produits/<int:pk>/', produits.detail, name='produits_detail'),
    path('produits/<int:pk>/modifier/', produits.modifier, name='produits_modifier'),
    path('produits/<int:pk>/supprimer/', produits.supprimer, name='produits_supprimer'),

    path('mouvements/', mouvements.liste, name='mouvements_liste'),
    path('mouvements/ajouter/', mouvements.ajouter, name='mouvements_ajouter'),

    path('commandes/', commandes.liste, name='commandes_liste'),
    path('commandes/creer/', commandes.creer, name='commandes_creer'),
    path('commandes/<int:pk>/', commandes.detail, name='commandes_detail'),
    path('commandes/<int:pk>/ajouter-ligne/', commandes.ajouter_ligne, name='commandes_ajouter_ligne'),
    path('commandes/<int:pk>/ligne/<int:ligne_id>/supprimer/', commandes.supprimer_ligne, name='commandes_supprimer_ligne'),

    path('fournisseurs/', fournisseurs.liste, name='fournisseurs_liste'),
    path('fournisseurs/ajouter/', fournisseurs.ajouter, name='fournisseurs_ajouter'),
    path('fournisseurs/<int:pk>/modifier/', fournisseurs.modifier, name='fournisseurs_modifier'),
    path('fournisseurs/<int:pk>/supprimer/', fournisseurs.supprimer, name='fournisseurs_supprimer'),

    path('alertes/', alertes.liste, name='alertes_liste'),
    path('alertes/<int:pk>/lire/', alertes.marquer_lu, name='alertes_lire'),
    path('alertes/tous-lus/', alertes.marquer_tous_lus, name='alertes_tous_lus'),

    path('rapports/inventaire/pdf/', rapports.inventaire_pdf, name='rapport_inventaire'),
    path('rapports/mouvements/pdf/', rapports.mouvements_pdf, name='rapport_mouvements'),
]
