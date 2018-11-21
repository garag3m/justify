
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


from .file_pdf import render_pdf

#--------Perfil------------
class Perfil(ListView):
    model = models.UUIDUser
    template_name = 'core/reposicao/perfil.html'

class PerfilUpdate(UpdateView):
    model = models.UUIDUser
    template_name = 'core/user/formup.html'
    success_url = reverse_lazy('core:login')
    form_class = forms.UUIDUserForm



#------Forms-----

## --- Form Replacement ---

class Replacement(CreateView):
    model = models.Solicitation
    template_name = 'core/reposicao/forms/formreposicao.html'
    success_url = reverse_lazy('reposicao:historico')
    fields = ['date_miss_start','date_miss_end', 'justification','file', 'reason','othes','team' ]

    def form_valid(self, form):
         obj = form.save(commit=False)
         obj.user = self.request.user
         for afile in self.request.FILES.getlist('original'):
            obj.file = afile
         obj.save()
         return super(Replacement, self).form_valid(form)

## --- Forms Anticipate ---

class Anticipate(CreateView):
    model = models.Solicitation
    template_name = 'core/reposicao/forms/formadiantamento.html'
    success_url = reverse_lazy('reposicao:historico')
    fields = ['date_miss_start','date_miss_end', 'justification','file', 'reason','othes','team']

    def form_valid(self, form):
         obj = form.save(commit=False)
         obj.user = self.request.user
         for afile in self.request.FILES.getlist('original'):
            obj.file = afile
         obj.save()
         return super(Anticipate, self).form_valid(form)

## --- Forms Exchange ---
class List(ListView):
    model = models.UUIDUser
    template_name = 'core/reposicao/listas/tabela.html'

    def get_queryset(self):
        if 'search' in self.request.GET:
            teachers = models.UUIDUser.objects.filter(first_name=self.request.GET['name'])
            return teachers
        else:
            return models.UUIDUser.objects.all()

class Message(DetailView):
    model = models.UUIDUser
    template_name = 'core/reposicao/forms/mensagem.html'

    def post(self, request, *args, **kwargs):
        profsolicitado = models.UUIDUser.objects.get(username=self.request.POST['solicitado'])
        a =  models.Exchange.objects.create(recipient=profsolicitado, sender=self.request.user,  mensagem=self.request.POST['mensagem'])
        a.save()
        return HttpResponseRedirect('/reposicao/historico/')


class Solicitationedit(UpdateView):
    model = models.Solicitation
    template_name = 'core/reposicao/forms/solicitacaoedit.html'
    success_url = reverse_lazy('reposicao:historico')
    fields = ['date_miss_start','date_miss_end', 'justification', 'reason','othes','team']

class MensagemUp(UpdateView):
    model = models.Exchange
    template_name = 'core/reposicao/aceitar/decisao.html'
    success_url = reverse_lazy('reposicao:historico')
    fields = ['status']


## --- Forms Refuse/Accept

class Accept(UpdateView):
    model = models.Authorization
    template_name = 'core/reposicao/aceitar/acite.html'
    success_url = reverse_lazy('reposicao:historico')
    fields = ['status','justification_Aceit']

    def get_context_data(self, **kwargs):
        kwargs['Solicitation'] = models.Solicitation.objects.all()
        return super(Accept, self).get_context_data(**kwargs)

    def get_queryset(self):
        return models.Authorization.objects.all()

## --- Forms Planning ---

class Planning(DetailView):
    model = models.Authorization
    template_name = 'core/reposicao/forms/planejamento.html'
    def post(self, request, *args, **kwargs):
        Solicitation = models.Solicitation.objects.get(id=self.request.POST['solicitation'])
        a =  models.Planning.objects.create(solicitation=Solicitation, components=self.request.POST['components'], date_class=self.request.POST['date_class'],time_class_first=self.request.POST['time_class_first'],time_class_last=self.request.POST['time_class_last'], date_restitution=self.request.POST['date_restitution'],time_restitution_first=self.request.POST['time_restitution_first'],time_restitution_last=self.request.POST['time_restitution_last'], descripition=self.request.POST['descripition'])
        a.save()
        return HttpResponseRedirect('/reposicao/historico/')


# -------- Historic --------


class Historic(ListView):
    model = models.Authorization
    template_name = 'core/reposicao/listas/historico.html'


    def get_context_data(self, **kwargs):
        kwargs['Planning'] = models.Planning.objects.all()
        if 'search' in self.request.GET:
            if self.request.GET['name']:
                try:
                    dado = int(self.request.GET['name'])
                    if self.request.GET['data_inicio'] :
                        if self.request.GET['data_fim'] :
                            kwargs['Solicitation'] = models.Solicitation.objects.filter(user__registration=self.request.GET['name'], date_miss_start = self.request.GET['data_inicio'], date_miss_end=self.request.GET['data_fim'] )
                            print(self.request.GET['data_fim'])
                        else:
                            kwargs['Solicitation'] = models.Solicitation.objects.filter(user__registration=self.request.GET['name'], date_miss_start = self.request.GET['data_inicio'])
                    else:
                        if self.request.GET['data_fim'] :
                            kwargs['Solicitation'] = models.Solicitation.objects.filter(user__registration=self.request.GET['name'], date_miss_end=self.request.GET['data_fim'] )
                        else:
                            kwargs['Solicitation'] = models.Solicitation.objects.filter(user__registration=self.request.GET['name'])
                except:
                    if self.request.GET['data_inicio'] :
                        if self.request.GET['data_fim'] :
                            kwargs['Solicitation'] = models.Solicitation.objects.filter(user__first_name=self.request.GET['name'], date_miss_start = self.request.GET['data_inicio'], date_miss_end=self.request.GET['data_fim'] )
                        else:
                            kwargs['Solicitation'] = models.Solicitation.objects.filter(user__first_name=self.request.GET['name'], date_miss_start = self.request.GET['data_inicio'] )
                    else:
                        if self.request.GET['data_fim'] :
                            kwargs['Solicitation'] = models.Solicitation.objects.filter(user__first_name=self.request.GET['name'], date_miss_end=self.request.GET['data_fim'] )
                        else:
                            kwargs['Solicitation'] = models.Solicitation.objects.filter(user__first_name=self.request.GET['name'])
            elif self.request.GET['data_inicio'] :
                if self.request.GET['data_fim'] :
                    kwargs['Solicitation'] = models.Solicitation.objects.filter(date_miss_start = self.request.GET['data_inicio'], date_miss_end=self.request.GET['data_fim'] )
                else:
                    kwargs['Solicitation'] = models.Solicitation.objects.filter(date_miss_start = self.request.GET['data_inicio'])
            elif self.request.GET['data_fim'] :
                kwargs['Solicitation'] = models.Solicitation.objects.filter( date_miss_end=self.request.GET['data_fim'] )
            else:
                kwargs['erro'] = True
                kwargs['Solicitation'] = models.Solicitation.objects.all()
            if len(kwargs['Solicitation']) == 0:
                kwargs['Solicitation'] = models.Solicitation.objects.all()
                kwargs['erro'] = True

        else:
            kwargs['Solicitation'] = models.Solicitation.objects.all()

        return super(Historic, self).get_context_data(**kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            return models.Authorization.objects.all()
        else:

            return models.Authorization.objects.filter(solicitation__user__first_name=self.request.user.first_name)



# ------- PDF ------

class Planning_PDF(View):
    model = models.Planning
    template_name = 'core/reposicao/pdf/planejamento_pdf.html'


    def get(self, request, pk):
        print (pk)
        dados = models.Planning.objects.filter(id = pk)
        pdf = render_pdf("core/reposicao/pdf/planejamento_pdf.html", {"dados": dados})
        return HttpResponse(pdf, content_type="application/pdf")
    def get_queryset (self):
        return models.Planning.objects.all()

class Solicitation_PDF(View):
    def get(self, request, *args, **kwargs):
        dados = models.Solicitation.objects.all()
        pdf = render_pdf("core/reposicao/pdf/historico_pdf.html", {"dados": dados})
        return HttpResponse(pdf, content_type="application/pdf")











