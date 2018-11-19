# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import include, path
from django.conf.urls import include, url

from . import views as core




app_name = 'reposicao'

urlpatterns = [

    #Usuários
     path('perfil/', core.Perfil.as_view(), name='perfil'),
     path('perfilup/<pk>/', core.PerfilUpdate.as_view(), name='perfilup'),


     #-----------------Formularios------------------------

     #formulario de Reposição
     path('reposicao/formrep/', core.Replacement.as_view(), name='formrep'),

     #formulario de Adiantamento de aula
     path('reposicao/formadianta/', core.Anticipate.as_view(), name='formadianta'),

     path('reposicao/aceitar/<pk>/', core.Accept.as_view(), name='aceitar'),

     #path('reposicao/aceitarform/<pk>/', core.AceitarCreateView.as_view(), name='aceitar-create'),

     #path('reposicao/negarform/<pk>/', core.NegarCreateView.as_view(), name='negar-create'),


     path('reposicao/historico/', core.Historic.as_view(), name='historico'),

     path('teste/', core.Solicitation_PDF.as_view(), name="aa"),

     path('reposicao/professores', core.List.as_view(), name='professores'),

     path('mensagem/<pk>/', core.Message.as_view(), name='mensagem'),

     path('reposicao/decisao/<pk>/', core.MensagemUp.as_view(), name='decisao'),

     path('reposicao/planejamento/<pk>/', core.Planning.as_view(), name='planejamento'),

     path('solicitacaoedit/<pk>/', core.Solicitationedit.as_view(), name='solicitacaoedit'),

     path('imprimirplanejamento/<pk>/', core.Planning_PDF.as_view(), name='imprimirplanejamento'),



]
