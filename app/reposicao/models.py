from django.db import models
from app.core.models import CreateUpdateModel, UUIDUser



class Motivo(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Motivo'
        verbose_name_plural='Motivos'

class Turma(models.Model):
    name = models.CharField('nome',max_length=100)
    period = models.IntegerField(verbose_name='Período')


    def __str__(self):
        return '%s-%i'%(self.name, self.period)


    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'



class Solicitacao(CreateUpdateModel):
    usuario = models.ForeignKey(UUIDUser,on_delete=models.CASCADE)
    justification = models.TextField(verbose_name='Justificativa')
    date_miss_start = models.DateField(verbose_name='Data da Falta Inicial')
    date_miss_end = models.DateField(verbose_name='Data da Falta Final')
    reason = models.ForeignKey(Motivo, on_delete = models.CASCADE, verbose_name='motivo')
    othes = models.CharField(max_length=200, null=True, blank=True, verbose_name='Outros' )
    team = models.ForeignKey(Turma, on_delete = models.CASCADE, verbose_name='turma')


    def __str__(self):
        return "%s" %(self.id)


    class Meta:
        verbose_name = 'Solicitação'
        verbose_name_plural = 'Solicitações'

class Autorizacao(CreateUpdateModel):

    STATUS = (
    (0, 'Negada'),
    (1, 'Andamento'),
    (2, 'Andamento'),
    (3, 'Aceita'))
    solicitation = models.ForeignKey(Solicitacao, on_delete=models.CASCADE)
    justification_Aceit = models.TextField(null=True, blank=True, verbose_name='Justificativa')
    status = models.IntegerField(choices=STATUS)

    def __str__(self):
        return '%s' %(self.status)

class Planejamento(CreateUpdateModel):
    solicitation = models.ForeignKey(Solicitacao, on_delete=models.CASCADE)
    components = models.CharField(max_length=100, verbose_name='Componente Curricular')
    date_class = models.DateField(verbose_name='Data da Aula')
    date_restitution = models.DateField(verbose_name='Data da Reposição')
    descripition  = models.TextField(verbose_name='Descrição')

    def __str__(self):
        return "%s" %(self.date_restitution)

    class Meta:
        verbose_name='Planejamento'
        verbose_name_plural = 'Planejamentos'

class Troca(CreateUpdateModel):
    STATUS = (
    (0, 'Negada'),
    (1, 'Andamento'),
    (2, 'Aceita'))
    solicitado = models.ForeignKey(UUIDUser,on_delete=models.CASCADE,related_name='trocas',verbose_name='solicitado')
    solicitante = models.ForeignKey(UUIDUser,on_delete=models.CASCADE, related_name='trocadeaula', verbose_name='solicitante')
    mensagem = models.TextField(verbose_name='mensagem')
    status = models.IntegerField(choices=STATUS, default=1)

    def __str__(self):
        return self.mensagem
