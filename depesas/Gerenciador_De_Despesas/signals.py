from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Categoria

@receiver(post_migrate)
def criar_categorias_padrao(sender, **kwargs):
    categorias = ["Moradia", "Alimentação", "Transporte", "Saúde", "Lazer", "Pessoais"]
    for nome in categorias:
        Categoria.objects.get_or_create(nome=nome)
