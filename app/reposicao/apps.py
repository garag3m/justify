from django.apps import AppConfig

class ReposicaoConfig(AppConfig):
    name = 'app.reposicao'

    def ready(self):
        from . import signals
