from django.urls import path
from . import views

urlpatterns = [
    path('Login/', views.Login, name='Login'),
    path('Principal/', views.Principal, name='Principal'),
]