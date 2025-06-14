from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import User
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Restaurante, Colaborador, Profile, Hotel, Obra
from django.core.exceptions import ValidationError
from .api_utils.viacep import buscar_endereco_por_cep

 #Cadastro Obra

class CadastroObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = [
            'nome', 'empresa', 'endereco', 
            'data_inicio', 'data_prevista_termino', 
            'data_real_termino', 'status', 'descricao'
        ]

        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome da Obra'}),
            'empresa': forms.TextInput(attrs={'placeholder': 'Nome da empresa responsável'}),
            'endereco': forms.TextInput(attrs={'placeholder': 'Endereço da Obra'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_prevista_termino': forms.DateInput(attrs={'type': 'date'}),
            'data_real_termino': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(),  # campo de escolha
            'descricao': forms.Textarea(attrs={'placeholder': 'Descrição da Obra'}),
        }


# Cadastro restaurantes
       
class CadastroRestauranteForm(forms.ModelForm):
    cep = forms.CharField(max_length=9, required=True)
    numero = forms.CharField(max_length=10, required=True)
    complemento = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Restaurante
        fields = ['nome', 'cnpj', 'telefone', 'responsavel']
    
    def clean(self):
        cleaned_data = super().clean()
        cep = cleaned_data.get('cep')
        numero = cleaned_data.get('numero')
        complemento = cleaned_data.get('complemento')

        if not cep:
            self.add_error('cep', 'O campo CEP é obrigatório.')
            return cleaned_data  # Ou levante um ValidationError geral

        endereco_api = buscar_endereco_por_cep(cep)
        if not endereco_api:
            raise forms.ValidationError("CEP inválido ou não encontrado.")

        endereco_formatado = f"{endereco_api['logradouro']}, {numero}"
        if complemento:
            endereco_formatado += f" - {complemento}"
        endereco_formatado += f", {endereco_api['bairro']}, {endereco_api['localidade']} - {endereco_api['uf']}, CEP {cep}"

        # Guarde o endereço formatado em um atributo extra no form para usar depois
        self.endereco_formatado = endereco_formatado

        return cleaned_data
 

# Cadastro Hotel 
class CadastroHotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['nome', 'cnpj', 'cidade', 'endereco', 'telefone', 'responsavel']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Cadatro usuarios
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="E-mail"
    )

    tipo = forms.ChoiceField(
        choices=Profile.TIPOS_USUARIO,
        label="Tipo de Usuário",
        required=True,
        widget=forms.Select(attrs={'onchange': 'toggleAdminPassword()'})
    )

    telefone = forms.CharField(
        max_length=15,
        required=False,
        label="Telefone"
    )

    admin_password = forms.CharField(
        required=False,
        label="Senha de Administrador (fornecida pelo RH)",
        widget=forms.PasswordInput(attrs={'style': 'display: none;'}),
        help_text="Obrigatório apenas para cadastro de administradores"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'tipo', 'telefone', 'admin_password')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Se o usuário atual não for admin, remova a opção de admin
        if self.request and not self.request.user.is_superuser:
            self.fields['tipo'].choices = [
                (value, label) for value, label in Profile.TIPOS_USUARIO 
                if value != 'admin'
            ]

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        admin_password = cleaned_data.get('admin_password')
        
        # Validação para cadastro de administrador
        if tipo == 'admin':
            # Obtenha a senha de admin das variáveis de ambiente
            rh_admin_password = "Senha123" 
            
            if not admin_password:
                raise ValidationError("Senha de administrador é obrigatória para este tipo de usuário")
            
            if admin_password != rh_admin_password:
                raise ValidationError("Senha de administrador incorreta")
            
            # Registro de auditoria
            if self.request:
                user = self.request.user
                print(f"Auditoria: Usuário {user.username} tentou criar um admin")  # Substitua por um logger real

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        # Se for admin, define como superuser/staff
        if self.cleaned_data['tipo'] == 'admin':
            user.is_staff = True
            user.is_superuser = True

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
            'nome', 'cpf', 'data_nascimento', 'telefone', 'endereco',
            'obra'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
        }
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        # Adicione aqui validações customizadas do CPF se necessário
        return cpf

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


