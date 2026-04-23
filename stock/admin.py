from django.contrib import admin
from .models import Categorie, Fournisseur, Produit, MouvementStock, Alerte, BonCommande, LigneCommande

admin.site.register(Categorie)
admin.site.register(Fournisseur)
admin.site.register(Produit)
admin.site.register(MouvementStock)
admin.site.register(Alerte)
admin.site.register(BonCommande)
admin.site.register(LigneCommande)
