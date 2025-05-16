from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from .models import Restaurante, Colaborador

# Cadatro restaurantes 
# class CadastroRestauranteForm(Restaurante):
        
class CadastroRestauranteForm(forms.ModelForm):
    class Meta:
        model = Restaurante
        fields = ['nome', 'cnpj', 'endereco', 'telefone', 'responsavel', 'capacidade', 'avaliacao', 'ativo']


# Cadatro usuarios 
class CadastroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class ColaboradorForm(forms.ModelForm):
    class Meta: 
        model = Colaborador
        fields = [
            'nome', 'cpf', 'rg', 'data_nascimento', 'sexo', 'estado_civil', 'telefone',
            'telefone_emergencia', 'cep', 'logradouro', 'numero', 'complemento', 'bairro',
            'cidade', 'estado', 'funcao', 'salario', 'data_admissao', 'data_demissao',
            'obra', 'ativo', 'foto', 'observacoes'
        ]
