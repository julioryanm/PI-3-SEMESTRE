from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from .models import Colaborador, Restaurante

# Cadatro restaurantes 
# class CadastroRestauranteForm(Restaurante):


# Cadatro usuarios 
class CadastroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

