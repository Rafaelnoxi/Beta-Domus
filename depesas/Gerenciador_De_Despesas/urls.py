from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name='principal'),
    path('perfil/', views.get_perfil, name='get_perfil'),
    path('perfil/atualizar/', views.atualizar_perfil, name='atualizar_perfil'),
    path('logout/', views.sair, name='logout'),
]
