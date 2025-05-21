from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from .models import Restaurante, Colaborador, Profile
 
# Cadatro restaurantes
# class CadastroRestauranteForm(Restaurante):
       
class CadastroRestauranteForm(forms.ModelForm):
    class Meta:
        model = Restaurante
        fields = ['nome', 'cnpj', 'endereco', 'telefone', 'responsavel']
 
 
# Cadatro usuarios
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="E-mail"
    )
 
    tipo = forms.ChoiceField(
        choices=Profile.TIPOS_USUARIO,
        label="Tipo de Usuário",
        required=True
    )
 
    telefone = forms.CharField(
        max_length=15,
        required=False,
        label="Telefone"
    )
 
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'tipo', 'telefone')
 
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
 
        if commit:
            user.save()
 
            Profile.objects.create(
                user=user,
                tipo=self.cleaned_data['tipo'],
                telefone=self.cleaned_data.get('telefone')
            )
 
        return user
       
class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = [
            'nome', 'cpf', 'data_nascimento', 'telefone', 'cidade',
            'obra', 'ativo', 'foto', 'observacoes'
        ]
