from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.test.signals import template_rendered
from django.core.mail import EmailMessage
from django.core import mail
from . import models, views, tasks
connection = mail.get_connection()
connection.open()

def create_Solicitation(sender, instance, created, **kwargs):
    var_edit = models.Authorization.objects.filter(solicitation = instance)
    if len(var_edit) > 0:
        for solicitations in var_edit:
            if solicitations.status == 0:
                authorization = models.Authorization.objects.filter(solicitation = instance).update(status=1)
                for object in models.Authorization.objects.all():
                    if object.solicitation == instance :
                        id = str(object.id)
                day = str(instance.date_miss_start.day)
                month = str(instance.date_miss_start.month)
                year = str(instance.date_miss_start.year)
                data = str('%s/%s/%s') %(day, month, year)
                day_end = str(instance.date_miss_end.day)
                month_end = str(instance.date_miss_end.month)
                year_end = str(instance.date_miss_end.year)
                data_end = str('%s/%s/%s') %(day_end, month_end, year_end)
                motivo = str(instance.reason.name)
                for cord in models.UUIDUser.objects.all():
                    for group in (cord.groups.all()):
                        if group == instance.team.area:
                            corden = str(cord.email)
                            team = str(instance.team)
                tasks.send_email.delay(data_end,data, motivo, id, team, corden )

    else:
        authorization = models.Authorization.objects.create(solicitation = instance, status = 1)
        authorization.save()
        for object in models.Authorization.objects.all():
            if object.solicitation == instance :
                id = str(object.id)
        day = str(instance.date_miss_start.day)
        month = str(instance.date_miss_start.month)
        year = str(instance.date_miss_start.year)
        data = str('%s/%s/%s') %(day, month, year)
        day_end = str(instance.date_miss_end.day)
        month_end = str(instance.date_miss_end.month)
        year_end = str(instance.date_miss_end.year)
        data_end = str('%s/%s/%s') %(day_end, month_end, year_end)
        motivo = str(instance.reason.name)
        for cord in models.UUIDUser.objects.all():
            for group in (cord.groups.all()):
                if group == instance.team.area:
                    corden = str(cord.email)
                    team = str(instance.team)
        tasks.send_email.delay(data_end,data, motivo, id, team, corden )

    # elif not created:
    #     autori = models.Authorization.objects.all()
    #     Authorization = models.Authorization.objects.filter(solicitation = instance).update(status=1)
    #     for object in autori:
    #         if object.solicitation == instance :
    #             id = str(object.id)
    #     day = str(instance.date_miss_start.day)
    #     month = str(instance.date_miss_start.month)
    #     year = str(instance.date_miss_start.year)
    #     data = str('%s/%s/%s') %(day, month, year)
    #     day_end = str(instance.date_miss_end.day)
    #     month_end = str(instance.date_miss_end.month)
    #     year_end = str(instance.date_miss_end.year)
    #     data_end = str('%s/%s/%s') %(day_end, month_end, year_end)
    #     motivo = str(instance.reason.name)
    #     tasks.send_email.delay(data_end,data, motivo, id)
        # for objeto in lista:
        #     if objeto.solicitation == instance:
        #         pk = str('127.0.0.1:8000/reposicao/aceitar/%s') %objeto.pk
        #         mensagen = str('Solicitacão de reposição de Aula \n Caro Coordenador, por meio desse email comunico que estarei ausente, pelo motivo de %s \n no período de %s à %s \n Para aceitar ou negar acesse o link : %s',)%(instance.reason,instance.date_miss_start,instance.date_miss_end,pk)

        # email = mail.EmailMessage(
        #     'Solicitacao De reposição',
        #     mensagen,
        #     'carlosabc436@gmail.com',
        #     ['megatronstall@gmail.com'],
        #     connection=connection,)
        # email.send()
        # connection.close()


post_save.connect(create_Solicitation, sender=models.Solicitation)



def Authorization(sender, instance, created, **kwargs):

        # if created:
        #     pk = str('127.0.0.1:8000/reposicao/alterar/%s') %(instance.pk)
        #     email = mail.EmailMessage(
        #         'Solicitacao Negada',
        #         pk,
        #         'carlosabc436@gmail.com',
        #         ['megatronstall@gmail.com'],999lo
        #         connection=connection,)
        #     email.send()
        #     connection.close()
        #     models.Authorization.objects.filter(id=instance.pk).update(status=(instance.status + 1))

        if instance.status == 0:
            autori = models.Solicitation.objects.all()
            for object in autori:
                if object == instance.solicitation :
                   pk = str(object.id)
            motivo = str(instance.justification_Aceit)
            tasks.negar_email.delay(motivo, pk)

        elif instance.status == 2 :
            pk = str(instance.id)
            day = str(instance.solicitation.date_miss_start.day)
            month = str(instance.solicitation.date_miss_start.month)
            year = str(instance.solicitation.date_miss_start.year)
            data = str('%s/%s/%s') %(day, month, year)
            day_end = str(instance.solicitation.date_miss_end.day)
            month_end = str(instance.solicitation.date_miss_end.month)
            year_end = str(instance.solicitation.date_miss_end.year)
            data_end = str('%s/%s/%s') %(day_end, month_end, year_end)
            motivo = str(instance.solicitation.reason.name)
            tasks.aceitar_email.delay(data_end,data, motivo, pk)

        elif instance.status == 3 :
            pk = str(instance.id)
            day = str(instance.solicitation.date_miss_start.day)
            month = str(instance.solicitation.date_miss_start.month)
            year = str(instance.solicitation.date_miss_start.year)
            data = str('%s/%s/%s') %(day, month, year)
            day_end = str(instance.solicitation.date_miss_end.day)
            month_end = str(instance.solicitation.date_miss_end.month)
            year_end = str(instance.solicitation.date_miss_end.year)
            data_end = str('%s/%s/%s') %(day_end, month_end, year_end)
            motivo = str(instance.solicitation.reason.name)
            tasks.aceitaremaildenovo.delay(data_end,data, motivo, pk)

        # elif (instance.status < 4):
        #     pk = str('127.0.0.1:8000/reposicao/aceitar/%s') %(instance.pk)
        #     email = mail.EmailMessage(
        #         'Hello',
        #         pk,
        #         'carlosabc436@gmail.com',
        #         ['carlosabc436@gmail.com'],
        #         connection=connection,)
        #     email.send()
        #     connection.close()
        #     models.Authorization.objects.filter(id=instance.pk).update(status=(instance.status + 1))


post_save.connect(Authorization, sender=models.Authorization)

def Exchange(sender, instance, created, **kwargs):
    if created:
        id = str(instance.pk)
        solicitado = str(instance.solicitado.email)
        solicitante = str(instance.solicitante.email)
        mensagem = str(instance.mensagem)
        tasks.mensagem.delay(id, solicitado, solicitante, mensagem)

    elif instance.status == 0:
        solicitado = str(instance.solicitado.email)
        firstname = str(instance.solicitado.first_name)
        solicitante = str(instance.solicitante.email)
        tasks.negar_mensagem.delay(solicitado, solicitante, firstname)

    elif instance.status == 2:
        solicitado = str(instance.solicitado.email)
        firstname = str(instance.solicitado.first_name)
        solicitante = str(instance.solicitante.email)
        tasks.aceitarmensagem.delay(solicitado, solicitante, firstname)

post_save.connect(Exchange, sender=models.Exchange)
