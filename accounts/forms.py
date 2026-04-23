from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import Utilisateur


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom d\'utilisateur'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )


class UtilisateurCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
