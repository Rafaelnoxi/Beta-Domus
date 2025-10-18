from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),  # Tela inicial antes do login
    path('login/', views.Login, name='login'),
    path('criar_conta/', views.CriarConta, name='criar_conta'),
    path('principal/', views.Principal, name='principal'),
    path('logout/', views.LogoutView, name='logout'),
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('despesa/adicionar/', views.adicionar_despesa, name='adicionar_despesa'),
    path('despesas/listar/', views.listar_despesas, name='listar_despesas'),
    path('despesa/excluir/<int:id>/', views.excluir_despesa, name='excluir_despesa'),
]
