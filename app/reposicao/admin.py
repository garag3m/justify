from django.contrib import admin
from .models import Motivo, Turma, Solicitacao, Planejamento, Autorizacao, Troca


admin.site.register(Motivo)
admin.site.register(Turma)
admin.site.register(Solicitacao)
admin.site.register(Planejamento)
admin.site.register(Autorizacao)
admin.site.register(Troca)
