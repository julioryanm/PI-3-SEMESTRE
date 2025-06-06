from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from .forms import CadastroRestauranteForm, ColaboradorForm, LoginForm, User, CadastroHotelForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Profile, Restaurante
from django.contrib.auth.models import Group,User
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.decorators import user_passes_test
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token
import logging

@api_view(['GET'])
def minha_api(request):
    if request.user.groups.filter(name='Encarregado').exists():
        raise PermissionDenied("Encarregados não podem acessar esta API.")
    return Response({"data": "Dados sensíveis"})

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

@api_view(['POST'])
@user_passes_test(is_admin)
def criar_usuario(request):
    # (apenas Admin pode acessar)
    return Response({"message": "Usuário criado com sucesso!"})


def login(request):
    if request.user.id is not None:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            return redirect('home')
        context = {'acesso negado': True}
        return render (request, 'login.html', {'form': form})
    return render(request, 'login.html', {'form': LoginForm()})

@csrf_protect
def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return render(request, 'logout.html')  # ou redirect('login')
    return redirect('home')  # se acessar via GET, redireciona



@login_required
def home(request):
    return render (request, 'home.html')


@login_required
def cadastro_colaborador(request):
    if request.method == 'POST':
        form = ColaboradorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Colaborador cadastrado com sucesso!')
            return redirect('cadastro_colaborador')  
    else:
        form = ColaboradorForm()

    return render(request, 'cadastro.html', {'form': form})

@login_required
def cadastroRestaurante(request):
    if request.method == 'POST':
        form = CadastroRestauranteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Restaurante cadastrado com sucesso!')
            return redirect('login')  
    else:
        form = CadastroRestauranteForm()

    return render(request, 'cadastroRestaurante.html', { 'form': form})
              
logger = logging.getLogger(__name__)


@login_required
def cadastroHotel(request):
    if request.method == 'POST':
        form = CadastroHotelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hotel cadastrado com sucesso!')
            return redirect('login')  
    else:
        form = CadastroHotelForm()

    return render(request, 'cadastroHotel.html', { 'form': form})

@login_required                  
def cadastrar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        tipo = request.POST.get('tipo')
        admin_password = request.POST.get('admin_password', '')

        # Validações
        if password != confirm_password:
            messages.error(request, 'As senhas não coincidem!')
            return redirect('cadastrar_usuario')

        # Verifica se o usuário já existe ANTES de tentar criar
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já está em uso!')
            return redirect('cadastrar_usuario')

        # Verificação para admin
        if tipo == 'admin' and admin_password != "Senha123": # Senha Supervisor
            messages.error(request, 'Senha de administrador incorreta!')
            return redirect('cadastrar_usuario')

        try:
            # Criação dos grupos 
            grupo_admin, _ = Group.objects.get_or_create(name='Administradores')
            grupo_encarregado, _ = Group.objects.get_or_create(name='Encarregados')

            # Cria o usuário
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            
            if tipo == 'admin':
                user.groups.add(grupo_admin)
                user.is_staff = True
                Token.objects.get_or_create(user=user)  # Token seguro
                logger.info(f'Novo admin criado: {username}')
            else:
                user.groups.add(grupo_encarregado)

            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('cadastrar_usuario')

        except Exception as e:
            logger.error(f'Erro ao criar usuário: {str(e)}')
            messages.error(request, f'Erro no sistema: {str(e)}')

    return render(request, 'cadastrar_usuario.html')

@login_required
def listar_colaboradores(request):
    return render (request, 'lista-colaborador.html')



@login_required
def listar_restaurantes(request, ):
    restaurante = Restaurante.objects.all()
    context = {'restaurante': restaurante}
    return render (request, 'lista-restaurantes.html', context)


@login_required
def listar_obras(request):
    return render (request, 'lista-obra.html')


@login_required
def relatorio(request):
    return render (request, 'relatorio.html')
