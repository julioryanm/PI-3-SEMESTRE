
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages



def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('login')  # ou outra URL válida
    else:
        form = UserCreationForm()
        
        
        return render(
        request,
        'cadastro.html',
        { 'cadastro': cadastro }
    )

