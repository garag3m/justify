
# -*- coding: utf-8 -*-
from django.views.generic import View

from django.contrib import admin
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from . import models, forms, tasks
from django.shortcuts import render


from .teste import render_pdf


class Home(TemplateView):
    template_name = 'home.html'

class Lista(ListView):
    model = models.UUIDUser
    template_name = 'core/reposicao/listas/tabela.html'

    def get_queryset(self):
        if 'search' in self.request.GET:
            teachers = models.UUIDUser.objects.filter(first_name=self.request.GET['name'])
            return teachers
        else:
            return models.UUIDUser.objects.all()


class Perfil(ListView):
    model = models.UUIDUser
    template_name = 'core/reposicao/perfil.html'

class PerfilUpdate(UpdateView):
    model = models.UUIDUser
    template_name = 'core/user/formup.html'
    success_url = reverse_lazy('core:login')
    form_class = forms.UUIDUserForm


class Reposicao(CreateView):
    model = models.Solicitacao
    template_name = 'core/reposicao/forms/formreposicao.html'
    success_url = reverse_lazy('reposicao:historico')
    fields = ['date_miss_start','date_miss_end', 'justification', 'reason','othes','team']

    def form_valid(self, form):
         obj = form.save(commit=False)
         obj.usuario = self.request.user
         obj.save()
         return super(Reposicao, self).form_valid(form)


class Adiantamento(CreateView):
    model = models.Solicitacao
    template_name = 'core/reposicao/forms/formadiantamento.html'
    success_url = reverse_lazy('reposicao:reposicao')
    fields = ['date_miss_start','date_miss_end', 'justification', 'reason','othes','team']

    def form_valid(self, form):
         obj = form.save(commit=False)
         obj.user = self.request.user
         obj.save()
         return super(Adiantamento, self).form_valid(form)

class Mensagem(DetailView):
    model = models.UUIDUser
    template_name = 'core/reposicao/forms/mensagem.html'

    def post(self, request, *args, **kwargs):
        profsolicitado = models.UUIDUser.objects.get(username=self.request.POST['solicitado'])
        a =  models.Troca.objects.create(solicitado=profsolicitado, solicitante=self.request.user,  mensagem=self.request.POST['mensagem'])
        a.save()
        return HttpResponseRedirect('/reposicao/historico/')

class Planejamento(DetailView):
    model = models.Autorizacao
    template_name = 'core/reposicao/forms/planejamento.html'
    def post(self, request, *args, **kwargs):
        solicitacao = models.Solicitacao.objects.get(id=self.request.POST['solicitation'])
        a =  models.Planejamento.objects.create(solicitation=solicitacao, components=self.request.POST['components'], date_class=self.request.POST['date_class'], date_restitution=self.request.POST['date_restitution'], descripition=self.request.POST['descripition'])
        a.save()
        return HttpResponseRedirect('/reposicao/historico/')

class Solicitacaoedit(UpdateView):
    model = models.Solicitacao
    template_name = 'core/reposicao/forms/solicitacaoedit.html'
    success_url = reverse_lazy('reposicao:historico')
    fields = ['date_miss_start','date_miss_end', 'justification', 'reason','othes','team']

class MensagemUp(UpdateView):
    model = models.Troca
    template_name = 'core/reposicao/aceitar/decisao.html'
    success_url = reverse_lazy('reposicao:historico')
    fields = ['status']




#class AceitarCreateView(UpdateView):
 #   model = models.Autorizacao
  #  template_name = 'core/reposicao/aceitar.html'
   # success_url = reverse_lazy('reposicao:reposicao')
    #fields = ['status']

    # def get_queryset(self):
    #     if 'aceita' in self.request.POST:
    #         autorizacao = models.Autorizacao.objects.get(id = self.request.POST['objeto'])
    #         status = int(autorizacao.status)
    #         status = status + 1
    #         print (status)
    #         models.Autorizacao.objects.filter(id = self.request.POST['objeto']).update(status=status)
    #     return models.Autorizacao.objects.all()




#class NegarCreateView(UpdateView):
 #   model = models.Autorizacao
  #  template_name = 'core/reposicao/negar.html'
   # success_url = reverse_lazy('reposicao:reposicao')
    #fields = ['status','justification_Aceit']




class Aceitar(UpdateView):
    model = models.Autorizacao
    template_name = 'core/reposicao/aceitar/acite.html'
    success_url = reverse_lazy('reposicao:historico')
    fields = ['status','justification_Aceit']

    def get_context_data(self, **kwargs):
        kwargs['solicitacao'] = models.Solicitacao.objects.all()
        return super(Aceitar, self).get_context_data(**kwargs)

    def get_queryset(self):
        # if 'aceita' in self.request.POST:
        #     autorizacao = models.Autorizacao.objects.get(id = self.request.POST['objeto'])
        #     status = int(autorizacao.status)
        #     status = status + 1
        #     print (status)
        #     models.Autorizacao.objects.filter(id = self.request.POST['objeto']).update(status=status)
        # if 'Negar' in self.request.POST:
        #     autorizacao = models.Autorizacao.objects.get(id = self.request.POST['objeto'])
        #     models.Autorizacao.objects.filter(id = self.request.POST['objeto']).update(status=0, justification_Aceit=self.request.POST['justificativa'])

        return models.Autorizacao.objects.all()

class Historico(ListView):
    model = models.Autorizacao
    template_name = 'core/reposicao/listas/historico.html'


    def get_context_data(self, **kwargs):
        kwargs['Planejamento'] = models.Planejamento.objects.all()
        if 'search' in self.request.GET:
            if self.request.GET['name']:
                try:
                    dado = int(self.request.GET['name'])
                    if self.request.GET['data_inicio'] :
                        if self.request.GET['data_fim'] :
                            kwargs['solicitacao'] = models.Solicitacao.objects.filter(usuario__registration=self.request.GET['name'], date_miss_start = self.request.GET['data_inicio'], date_miss_end=self.request.GET['data_fim'] )
                            print(self.request.GET['data_fim'])
                        else:
                            kwargs['solicitacao'] = models.Solicitacao.objects.filter(usuario__registration=self.request.GET['name'], date_miss_start = self.request.GET['data_inicio'])
                    else:
                        if self.request.GET['data_fim'] :
                            kwargs['solicitacao'] = models.Solicitacao.objects.filter(usuario__registration=self.request.GET['name'], date_miss_end=self.request.GET['data_fim'] )
                        else:
                            kwargs['solicitacao'] = models.Solicitacao.objects.filter(usuario__registration=self.request.GET['name'])
                except:
                    if self.request.GET['data_inicio'] :
                        if self.request.GET['data_fim'] :
                            kwargs['solicitacao'] = models.Solicitacao.objects.filter(usuario__first_name=self.request.GET['name'], date_miss_start = self.request.GET['data_inicio'], date_miss_end=self.request.GET['data_fim'] )
                        else:
                            kwargs['solicitacao'] = models.Solicitacao.objects.filter(usuario__first_name=self.request.GET['name'], date_miss_start = self.request.GET['data_inicio'] )
                    else:
                        if self.request.GET['data_fim'] :
                            kwargs['solicitacao'] = models.Solicitacao.objects.filter(usuario__first_name=self.request.GET['name'], date_miss_end=self.request.GET['data_fim'] )
                        else:
                            kwargs['solicitacao'] = models.Solicitacao.objects.filter(usuario__first_name=self.request.GET['name'])
            elif self.request.GET['data_inicio'] :
                if self.request.GET['data_fim'] :
                    kwargs['solicitacao'] = models.Solicitacao.objects.filter(date_miss_start = self.request.GET['data_inicio'], date_miss_end=self.request.GET['data_fim'] )
                else:
                    kwargs['solicitacao'] = models.Solicitacao.objects.filter(date_miss_start = self.request.GET['data_inicio'])
            elif self.request.GET['data_fim'] :
                kwargs['solicitacao'] = models.Solicitacao.objects.filter( date_miss_end=self.request.GET['data_fim'] )
            else:
                kwargs['erro'] = True
                kwargs['solicitacao'] = models.Solicitacao.objects.all()
            if len(kwargs['solicitacao']) == 0:
                kwargs['solicitacao'] = models.Solicitacao.objects.all()
                kwargs['erro'] = True

        else:
            kwargs['solicitacao'] = models.Solicitacao.objects.all()

        return super(Historico, self).get_context_data(**kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            return models.Autorizacao.objects.all()
        else:

            return models.Autorizacao.objects.filter(solicitation__usuario__first_name=self.request.user.first_name)


class ImprimirPlanejamento(View):
    model = models.Planejamento
    template_name = 'core/reposicao/pdf/planejamento_pdf.html'


    def get(self, request, *args, **kwargs):
        dados = self.request.content_params
        pdf = render_pdf("core/reposicao/pdf/planejamento_pdf.html", {"dados": dados})
        return HttpResponse(pdf, content_type="application/pdf")
    def get_queryset (self):
        return models.Planejamento.objects.all()

class Teste(View):
    def get(self, request, *args, **kwargs):
        dados = models.Solicitacao.objects.all()
        pdf = render_pdf("core/reposicao/pdf/historico_pdf.html", {"dados": dados})
        return HttpResponse(pdf, content_type="application/pdf")










#def historico(request):
#    template_name = 'core/reposicao/historico.html'
#    return render(request,template_name)
#
#def adiantamento(request):
#    template_name = 'core/reposicao/formadiantamento.html'
#    return render(request,template_name)

#def troca(request):
#    template_name = 'core/reposicao/formtroca.html'
#    return render(request,template_name)
