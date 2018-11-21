# Generated by Django 2.0.7 on 2018-11-21 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Authorization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='atualizado em')),
                ('justification_Aceit', models.TextField(blank=True, null=True, verbose_name='Justificativa')),
                ('status', models.IntegerField(choices=[(0, 'Negada'), (1, 'Andamento'), (2, 'Andamento'), (3, 'Aceita')])),
            ],
            options={
                'verbose_name': 'Autorização',
                'verbose_name_plural': 'Autorizações',
            },
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='atualizado em')),
                ('Message', models.TextField(verbose_name='mensagem')),
                ('status', models.IntegerField(choices=[(0, 'Negada'), (1, 'Andamento'), (2, 'Aceita')], default=1)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trocas', to=settings.AUTH_USER_MODEL, verbose_name='solicitado')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trocadeaula', to=settings.AUTH_USER_MODEL, verbose_name='solicitante')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Planning',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='atualizado em')),
                ('components', models.CharField(max_length=100, verbose_name='Componente Curricular')),
                ('date_class', models.DateField(verbose_name='Data da Aula')),
                ('time_class_first', models.TimeField(verbose_name='Início da Aula')),
                ('time_class_last', models.TimeField(verbose_name='Término da Aula')),
                ('date_restitution', models.DateField(verbose_name='Data da Reposição')),
                ('time_restitution_first', models.TimeField(verbose_name='Início da Falta')),
                ('time_restitution_last', models.TimeField(verbose_name='Término da Falta')),
                ('descripition', models.TextField(verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Planejamento',
                'verbose_name_plural': 'Planejamentos',
            },
        ),
        migrations.CreateModel(
            name='Reason',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='atualizado em')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Motivo',
                'verbose_name_plural': 'Motivos',
            },
        ),
        migrations.CreateModel(
            name='Solicitation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='atualizado em')),
                ('justification', models.TextField(verbose_name='Justificativa')),
                ('file', models.FileField(blank=True, null=True, upload_to='original', verbose_name='Arquivo')),
                ('date_miss_start', models.DateField(verbose_name='Data da Falta Inicial')),
                ('date_miss_end', models.DateField(verbose_name='Data da Falta Final')),
                ('othes', models.CharField(blank=True, max_length=200, null=True, verbose_name='Outros')),
                ('reason', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reason', to='reposicao.Reason', verbose_name='motivo')),
            ],
            options={
                'verbose_name': 'Solicitação',
                'verbose_name_plural': 'Solicitações',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='atualizado em')),
                ('name', models.CharField(max_length=100, verbose_name='nome')),
                ('period', models.IntegerField(verbose_name='Período')),
            ],
            options={
                'verbose_name': 'Turma',
                'verbose_name_plural': 'Turmas',
            },
        ),
        migrations.AddField(
            model_name='solicitation',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='reposicao.Team', verbose_name='turma'),
        ),
        migrations.AddField(
            model_name='solicitation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='planning',
            name='solicitation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reposicao.Solicitation'),
        ),
        migrations.AddField(
            model_name='authorization',
            name='solicitation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reposicao.Solicitation'),
        ),
    ]
