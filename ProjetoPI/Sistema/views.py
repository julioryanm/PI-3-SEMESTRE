from django.shortcuts import render, redirect
from .forms import ColaboradorForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Restaurante cadastrado com sucesso!')
            return redirect('login')  # Redireciona após sucesso
    else:
        form = UserCreationForm()

    return render(request, 'cadastroRestaurante.html', { 'form': form
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
def login(request):
    return render(request, 'login.html')

def home (request):
    return render(request, 'home.html')
