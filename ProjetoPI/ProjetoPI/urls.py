from django.contrib import admin
from django.urls import path
from Sistema import views
from django.conf import settings
from django.conf.urls.static import static

from Sistema.views import (
    home, login,
    cadastroRestaurante,
    cadastro_colaborador,
    cadastrar_usuario,)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastroRestaurante/', cadastroRestaurante, name='cadastroRestaurante'),
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cadastro/', cadastro_colaborador, name='cadastro'),
    path('cadastrar-usuario/', cadastrar_usuario, name='cadastrar_usuario'),
    path('relatorio/', views.relatorio, name='relatorio'), 
    path('listar-restaurantes/', views.listar_restaurantes, name='listar-restaurantes'),
    path('listar-obras/', views.listar_obras, name='listar-obras'),
    path('listar-colaboradores/', views.lista_colaboradores, name='listar-colaboradores'),
    path('editar-colaborador/<int:id>/', views.editar_colaborador, name='editar-colaborador'),
    path('excluir-colaborador/<int:id>/', views.excluir_colaborador, name='excluir-colaborador'),
    path('listar-hoteis/', views.listar_hoteis, name='listar-hoteis'), 
    path('cadastrar-hotel/', views.cadastro_hotel, name='cadastrar-hotel'), 
    path('deletar/', views.deletar_generico, name='deletar-generico'),
    path('editar-hotel/<int:id>/', views.editar_hotel, name='editar-hotel'),
    path('editar/', views.redirecionar_edicao_hotel, name='redirecionar-edicao-hotel'),    
]
