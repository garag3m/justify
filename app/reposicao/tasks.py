from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.test.signals import template_rendered
from django.core.mail import EmailMessage
from django.core import mail
from . import models
from . import views
connection = mail.get_connection()
connection.open()




@shared_task
def send_email(data_end,data, motivo, id):
    print ('objeto ola')
    pk = str('127.0.0.1:8000/reposicao/aceitar/%s')%id
    mensagen = str('Solicitacão de reposição de Aula \n Caro Coordenador, por meio desse email comunico que estarei ausente, pelo motivo de %s \n no período de %s à %s \n Para aceitar ou negar acesse o link : %s',)%(motivo, data, data_end, pk)
    email = mail.EmailMessage(
        'Solicitacao De reposição',
        mensagen,
        'carlosabc436@gmail.com',
        ['megatronstall@gmail.com'],
        connection=connection,)
    email.send()

@shared_task
def negar_email(justification_Aceit, id):
    pk = str('Caro discente sua Solicitacao de Reposicao foi negada pelos seguintes motivos:'
    '\n \n \n %s'
    '\n \n  Acesse o link para a alterações necessarias'
    '\n \n \n 127.0.0.1:8000/reposicao/alterar/%s') %(justification_Aceit, id)
    email = mail.EmailMessage(
        'Solicitacao Negada',
        pk,
        'carlosabc436@gmail.com',
        ['megatronstall@gmail.com'],
        connection=connection,)
    email.send()

@shared_task
def aceitar_email(d,dat, mot, id):
    pk = str('127.0.0.1:8000/reposicao/aceitar/%s')%id
    mensagen = str('Solicitacão de reposição de Aula \n Caro Coordenador, por meio desse email comunico que estarei ausente, pelo motivo de %s \n no período de %s à %s \n Para aceitar ou negar acesse o link : %s',)%(mot, dat, d, pk)
    email = mail.EmailMessage(
        'Solicitacao De reposição',
        mensagen,
        'carlosabc436@gmail.com',
        ['carlosabc436@gmail.com'],
        connection=connection,)
    email.send()

@shared_task
def aceitaremaildenovo(d,dat, mot, id):
    mensagen = str('Solicitacão de reposição de Aula \n Caro Coordenador, por meio desse email comunico que estarei ausente, pelo motivo de %s \n no período de %s à %s ')%(mot, dat, d)
    email = mail.EmailMessage(
        'Solicitacao de Reposição',
        mensagen,
        'carlosabc436@gmail.com',
        ['carlosabc436@gmail.com'],
        connection=connection,)
    email.send()
    pk = str('127.0.0.1:8000/reposicao/planejamento/%s')%id
    mensagem = str(' Caro Docente, por meio desse email comunico que sua solicitação de reposição foi aprovada. \n Para preencher o planejamento de aula acesse o link : %s',)%(pk)
    email1 = mail.EmailMessage(
        'Solicitacao de Reposição',
        mensagem,
        'carlosabc436@gmail.com',
        ['carlosabc436@gmail.com'],
        connection=connection,)
    email1.send()

@shared_task
def mensagem(id, solicitado, solicitante, mensagem):
    pk = str('127.0.0.1:8000/reposicao/decisao/%s')%id
    mensagem = str('Solicitação de Troca de Aula \n Mensagem do professor solicitante \n %s  \n Para aceitar ou negar acesse o link : %s',)%(mensagem, pk)
    email = mail.EmailMessage(
        'Solicitacao de Troca de Aula',
        mensagem,
        solicitante,
        [solicitado],
        connection=connection,)
    email.send()

@shared_task
def negar_mensagem( solicitado, solicitante, firstname):
    mensagem = str('Resposta da solicitação de troca de aula \n O professor %s negou sua solicitação de troca de aula. ',)%(firstname)
    email = mail.EmailMessage(
        'Solicitacao de Troca de Aula',
        mensagem,
        solicitado,
        [solicitante],
        connection=connection,)
    email.send()

@shared_task
def aceitarmensagem(solicitado, solicitante, firstname):
    print ('qualquer coisa funciona')
    pk = str('127.0.0.1:8000/reposicao/formrep/')
    mensagem = str('Resposta da solicitação de troca de aula \n O professor %s aceitou sua solicitação de troca de aula.  \n Para enviar sua solicitação de reposição acesse o link : %s',)%(firstname, pk)
    email = mail.EmailMessage(
        'Solicitacao de Troca de Aula',
        mensagem,
        solicitado,
        [solicitante],
        connection=connection,)
    email.send()
connection.close()
