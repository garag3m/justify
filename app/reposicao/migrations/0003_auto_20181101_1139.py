# Generated by Django 2.0.7 on 2018-11-01 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reposicao', '0002_remove_planejamento_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacao',
            name='reason',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reposicao.Motivo', verbose_name='motivo'),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reposicao.Turma', verbose_name='turma'),
        ),
    ]