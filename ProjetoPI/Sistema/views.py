from django.shortcuts import render, redirect
from .forms import ColaboradorForm, CadastroUsuarioForm, CadastroRestauranteForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Profile

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


def cadastroRestaurante(request):
    if request.method == 'POST':
        form = CadastroRestauranteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Restaurante cadastrado com sucesso!')
            return redirect('login')  # Redireciona após sucesso
    else:
        form = CadastroRestauranteForm()

    return render(request, 'cadastroRestaurante.html', { 'form': form})
                  
def cadastrar_usuario(request):
    if request.method == 'POST':
       
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect ('login')
        else:
            form = CadastroUsuarioForm()
        return render (request,  'cadastrar_usuario.html', {'form': form})


def login(request):
    return render(request, 'login.html')

def home (request):
    return render(request, 'home.html')
