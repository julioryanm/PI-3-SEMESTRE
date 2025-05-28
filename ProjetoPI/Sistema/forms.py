from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import User
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Restaurante, Colaborador, Profile, Hotel
 
# Cadatro restaurantes
# class CadastroRestauranteForm(Restaurante):
       
class CadastroRestauranteForm(forms.ModelForm):
    class Meta:
        model = Restaurante
        fields = ['nome', 'cnpj', 'endereco', 'telefone', 'responsavel']
 
class CadastroHotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['nome', 'cnpj', 'cidade', 'endereco', 'telefone', 'responsavel']
 
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

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        labels = {
            'email': 'E-Mail:', 
            'password': 'Senha:',
        }

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder':'Digite seu e-mail'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control',
                                                   'placeholder':'Digite sua senha'}),
        }
        error_messages = {
            'email': {
                'required': ("Informe o e-mail."),
            },
        }

        
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@castrosconstrutora.com'):
            raise ValidationError('Informe seu e-mail corporativo.')
        return self.cleaned_data['email']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise ValidationError("Usuário com esse e-mail não encontrado.")

            user = authenticate(username=user.username, password=password)
            if user is None:
                raise ValidationError("Senha incorreta para o e-mail informado.")

            self.user = user


