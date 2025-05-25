from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from .forms import CadastroRestauranteForm, ColaboradorForm, LoginForm, User
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Profile




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

@login_required                  
def cadastrar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        tipo = request.POST.get('tipo')


        if password != confirm_password:
            messages.error(request, 'As senhas não coincidem!')
            return redirect('cadastrar_usuario')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe!')
            return redirect('cadastrar_usuario')

        if email and User.objects.filter(email=email).exists():
            messages.error(request, 'E-mail já cadastrado!')
            return redirect('cadastrar_usuario')


        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )


            Profile.objects.create(
                user=user,
                tipo=tipo
            )

            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('cadastrar_usuario') 

        except Exception as e:
            messages.error(request, f'Erro ao cadastrar usuário: {str(e)}')
            return redirect('cadastrar_usuario')


    return render(request, 'cadastrar_usuario.html')



@login_required
def relatorio(request):
    return render (request, 'relatorio.html')


