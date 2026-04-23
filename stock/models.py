from django.db import models
from django.conf import settings
from django.utils import timezone


class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name_plural = "Catégories"
        ordering = ['nom']


class Fournisseur(models.Model):
    nom = models.CharField(max_length=150)
    adresse = models.TextField(blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['nom']


class Produit(models.Model):
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    reference = models.CharField(max_length=50, unique=True)
    code_barre = models.CharField(max_length=50, unique=True, blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_stock = models.PositiveIntegerField(default=0)
    seuil_alerte = models.PositiveIntegerField(default=10)
    categorie = models.ForeignKey(
        Categorie, on_delete=models.PROTECT, related_name='produits'
    )
    fournisseur = models.ForeignKey(
        Fournisseur, on_delete=models.PROTECT, related_name='produits'
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    def is_low_stock(self):
        return self.quantite_stock <= self.seuil_alerte

    def valeur_stock(self):
        return self.quantite_stock * self.prix

    def __str__(self):
        return f"{self.nom} [{self.reference}]"

    class Meta:
        ordering = ['nom']


class MouvementStock(models.Model):
    TYPE_CHOICES = [
        ('entree', 'Entrée'),
        ('sortie', 'Sortie'),
        ('ajustement', 'Ajustement'),
    ]
    produit = models.ForeignKey(
        Produit, on_delete=models.PROTECT, related_name='mouvements'
    )
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='mouvements'
    )
    type_mouvement = models.CharField(max_length=20, choices=TYPE_CHOICES)
    quantite = models.IntegerField()
    motif = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.type_mouvement == 'entree':
            self.produit.quantite_stock += self.quantite
        elif self.type_mouvement == 'sortie':
            self.produit.quantite_stock -= self.quantite
        elif self.type_mouvement == 'ajustement':
            self.produit.quantite_stock += self.quantite
        self.produit.save()
        super().save(*args, **kwargs)
        check_and_create_alerte(self.produit)

    def __str__(self):
        return f"{self.type_mouvement} — {self.produit.nom} ({self.quantite})"

    class Meta:
        ordering = ['-date']


class Alerte(models.Model):
    produit = models.ForeignKey(
        Produit, on_delete=models.CASCADE, related_name='alertes'
    )
    message = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Alerte: {self.produit.nom} — {self.date.strftime('%d/%m/%Y')}"

    class Meta:
        ordering = ['-date']


class BonCommande(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('envoye', 'Envoyé'),
        ('recu', 'Reçu'),
        ('annule', 'Annulé'),
    ]
    fournisseur = models.ForeignKey(
        Fournisseur, on_delete=models.PROTECT, related_name='bons_commande'
    )
    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='bons_commande'
    )
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    notes = models.TextField(blank=True)

    def total(self):
        return sum(ligne.sous_total() for ligne in self.lignes.all())

    def __str__(self):
        return f"BC-{self.pk:04d} — {self.fournisseur.nom} ({self.statut})"

    class Meta:
        ordering = ['-date_commande']
        verbose_name = "Bon de commande"
        verbose_name_plural = "Bons de commande"


class LigneCommande(models.Model):
    bon_commande = models.ForeignKey(
        BonCommande, on_delete=models.CASCADE, related_name='lignes'
    )
    produit = models.ForeignKey(
        Produit, on_delete=models.PROTECT, related_name='lignes_commande'
    )
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def sous_total(self):
        return self.quantite * self.prix_unitaire

    def __str__(self):
        return f"{self.produit.nom} × {self.quantite}"

    class Meta:
        ordering = ['id']


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
