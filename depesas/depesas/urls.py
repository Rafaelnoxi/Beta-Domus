from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('Gerenciador_De_Despesas.urls')),
    path('admin/', admin.site.urls),
]
