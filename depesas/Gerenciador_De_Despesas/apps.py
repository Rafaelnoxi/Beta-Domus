from django.apps import AppConfig

class GerenciadorDeDespesasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Gerenciador_De_Despesas'

    def ready(self):
        import Gerenciador_De_Despesas.signals
