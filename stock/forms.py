from django import forms
from .models import Produit, MouvementStock, BonCommande, LigneCommande, Categorie, Fournisseur


class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la catégorie'}),
        }


class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom', 'adresse', 'telephone', 'email']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Adresse'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'reference', 'code_barre', 'prix', 'quantite_stock', 'seuil_alerte', 'categorie', 'fournisseur']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du produit'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Référence unique'}),
            'code_barre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code-barres (optionnel)'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Prix unitaire'}),
            'quantite_stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantité initiale'}),
            'seuil_alerte': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Seuil d\'alerte'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'fournisseur': forms.Select(attrs={'class': 'form-control'}),
        }


class MouvementStockForm(forms.ModelForm):
    class Meta:
        model = MouvementStock
        fields = ['produit', 'type_mouvement', 'quantite', 'motif']
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-control'}),
            'type_mouvement': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantité'}),
            'motif': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motif (optionnel)'}),
        }


class BonCommandeForm(forms.ModelForm):
    class Meta:
        model = BonCommande
        fields = ['fournisseur', 'notes']
        widgets = {
            'fournisseur': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notes (optionnel)'}),
        }


class LigneCommandeForm(forms.ModelForm):
    class Meta:
        model = LigneCommande
        fields = ['produit', 'quantite', 'prix_unitaire']
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantité'}),
            'prix_unitaire': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Prix unitaire'}),
        }


class BonCommandeStatusForm(forms.ModelForm):
    class Meta:
        model = BonCommande
        fields = ['statut']
        widgets = {
            'statut': forms.Select(attrs={'class': 'form-control'}),
        }
