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
def send_email(data_end,data, motivo, id,coordenador):
    pk = str('127.0.0.1:8000/reposicao/aceitar/%s')%id
    mensagen = str('Solicitacão de reposição de Aula \n Caro Coordenador, por meio desse email comunico que estarei ausente, pelo motivo de %s \n no período de %s à %s \n Para aceitar ou negar acesse o link : %s',)%(motivo, data, data_end, pk)
    email = mail.EmailMessage(
        'Solicitacao De reposição',
        mensagen,
        'carlosabc436@gmail.com',
        [coordenador],
        connection=connection,)
    email.send()

@shared_task
def negar_email(justification_Aceit, id, email):
    pk = str('Caro discente sua Solicitacao de Reposicao foi negada pelos seguintes motivos:'
    '\n \n \n %s'
    '\n \n  Acesse o link para a alterações necessarias'
    '\n \n \n 127.0.0.1:8000/reposicao/alterar/%s') %(justification_Aceit, id)
    email = mail.EmailMessage(
        'Solicitacao Negada',
        pk,
        'carlosabc436@gmail.com',
        [email],
        connection=connection,)
    email.send()

@shared_task
def aceitar_email(d,dat, mot, id, coordenador, turma):
    pk = str('127.0.0.1:8000/reposicao/aceitar/%s')%id
    mensagen = str('Solicitacão de reposição de Aula \n Caro Coordenador, por meio desse email comunico que estarei ausente, pelo motivo de %s \n no período de %s à %s \n Para aceitar ou negar acesse o link : %s',)%(mot, dat, d, pk)
    email = mail.EmailMessage(
        'Solicitacao De reposição',
        mensagen,
        'carlosabc436@gmail.com',
        [coordenador],
        connection=connection,)
    email.send()

@shared_task
def Solicitation_acept( id, email):
    pk = str('127.0.0.1:8000/reposicao/planejamento/%s') %(id)
    mensagen = str('Solicitação de reposição de Aula \n Caro professor, sua Solicitação de reposição de aula foi aprovada\n Entre no site %s  para concluir o Planejamento da reposição')%(pk)
    email = mail.EmailMessage(
        'Solicitacao de Reposição',
        mensagen,
        'carlosabc436@gmail.com',
        [email],
        connection=connection,)

@shared_task
def acept(d,dat, mot, id, assistente):
    mensagen = str('Solicitacão de reposição de Aula \n Caro Coordenador, por meio desse email comunico que estarei ausente, pelo motivo de %s \n no período de %s à %s.')%(mot, dat, d,)
    email = mail.EmailMessage(
        'Solicitacao de Reposição',
        mensagen,
        'carlosabc436@gmail.com',
        [assistente],
        connection=connection,)

@shared_task
def mensagem(id, solicitado, solicitante, mensagem):
    pk = str('127.0.0.1:8000/reposicao/decisao/%s')%id
    mensagem = str('Solicitação de Troca de Aula \n Mensagem do professor %s \n %s  \n Para aceitar ou negar acesse o link : %s',)%(solicitante, mensagem, pk)
    email = mail.EmailMessage(
        'Solicitacao de Troca de Aula',
        mensagem,
        'carlosabc436@gmail.com',
        [solicitado],
        connection=connection,)
    email.send()

@shared_task
def negar_mensagem( solicitado, solicitante, firstname):
    mensagem = str('Resposta da solicitação de troca de aula \n O professor %s negou sua solicitação de troca de aula. ',)%(firstname)
    email = mail.EmailMessage(
        'Solicitacao de Troca de Aula',
        mensagem,
        'carlosabc436@gmail.com',
        [solicitante],
        connection=connection,)
    email.send()

@shared_task
def aceitarmensagem(solicitado, solicitante, firstname):
    pk = str('127.0.0.1:8000/reposicao/formrep/')
    mensagem = str('Resposta da solicitação de troca de aula \n O professor %s aceitou sua solicitação de troca de aula.  \n Para enviar sua solicitação de reposição acesse o link : %s',)%(firstname, pk)
    email = mail.EmailMessage(
        'Solicitacao de Troca de Aula',
        mensagem,
        'carlosabc436@gmail.com',
        [solicitante],
        connection=connection,)
    email.send()

    
connection.close()
