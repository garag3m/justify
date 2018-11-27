from django.db import models
from app.core.models import CreateUpdateModel, UUIDUser
from django.contrib.auth.models import Group



class Reason(CreateUpdateModel):
    name = models.CharField(max_length=100, verbose_name='Nome')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Motivo'
        verbose_name_plural='Motivos'

class Team(CreateUpdateModel):
    name = models.CharField('nome',max_length=100)
    period = models.IntegerField(verbose_name='Período')
    area = models.ForeignKey(Group, blank=True, related_name="area_cood", related_query_name="area", on_delete=models.CASCADE)


    def __str__(self):
        return '%s-%i'%(self.name, self.period)


    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'



class Solicitation(CreateUpdateModel):
    user = models.ForeignKey(UUIDUser,on_delete=models.CASCADE)
    justification = models.TextField(verbose_name='Justificativa')
    file = models.FileField(verbose_name='Arquivo', null=True, blank=True, upload_to='original')
    date_miss_start = models.DateField(verbose_name='Data da Falta Inicial')
    date_miss_end = models.DateField(verbose_name='Data da Falta Final')
    reason = models.ForeignKey(Reason, on_delete = models.CASCADE, verbose_name='motivo', related_name='reason')
    othes = models.CharField(max_length=200, null=True, blank=True, verbose_name='Outros' )
    team = models.ForeignKey(Team, on_delete = models.CASCADE, verbose_name='turma', related_name='team')


    def __str__(self):
        return "%s" %(self.justification)


    class Meta:
        verbose_name = 'Solicitação'
        verbose_name_plural = 'Solicitações'

class Authorization(CreateUpdateModel):

    STATUS = (
    (0, 'Negada'),
    (1, 'Andamento'),
    (2, 'Andamento'),
    (3, 'Aceita'))
    solicitation = models.ForeignKey(Solicitation, on_delete=models.CASCADE)
    justification_Aceit = models.TextField(null=True, blank=True, verbose_name='Justificativa')
    status = models.IntegerField(choices=STATUS)

    def __str__(self):
        return '%s' %(self.status)

    class Meta:
        verbose_name = 'Autorização'
        verbose_name_plural = 'Autorizações'

class Planning(CreateUpdateModel):
    solicitation = models.ForeignKey(Solicitation, on_delete=models.CASCADE)
    components = models.CharField(max_length=100, verbose_name='Componente Curricular')
    date_class = models.DateField(verbose_name='Data da Aula')
    time_class_first = models.TimeField(verbose_name='Início da Aula')
    time_class_last = models.TimeField(verbose_name='Término da Aula')
    date_restitution = models.DateField(verbose_name='Data da Reposição')
    time_restitution_first = models.TimeField(verbose_name='Início da Falta')
    time_restitution_last = models.TimeField(verbose_name='Término da Falta')
    descripition = models.TextField(verbose_name='Descrição')

    def __str__(self):
        return "%s" %(self.date_restitution)

    class Meta:
        verbose_name='Planejamento'
        verbose_name_plural = 'Planejamentos'

class Exchange(CreateUpdateModel):
    STATUS = (
    (0, 'Negada'),
    (1, 'Andamento'),
    (2, 'Aceita'))
    recipient = models.ForeignKey(UUIDUser,on_delete=models.CASCADE,related_name='trocas',verbose_name='solicitado')
    sender = models.ForeignKey(UUIDUser,on_delete=models.CASCADE, related_name='trocadeaula', verbose_name='solicitante')
    Message = models.TextField(verbose_name='mensagem')
    status = models.IntegerField(choices=STATUS, default=1)

    def __str__(self):
        return self.mensagem

    class Mata:
        verbose_name = 'Troca de Aula'
        verbose_name_plural = 'Troca de Aulas'
