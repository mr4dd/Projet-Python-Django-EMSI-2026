from django.contrib.auth.models import AbstractUser
from django.db import models


class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('gestionnaire', 'Gestionnaire'),
        ('employe', 'Employé'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employe')

    def is_admin(self):
        return self.role == 'admin'

    def is_gestionnaire(self):
        return self.role in ('admin', 'gestionnaire')

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
