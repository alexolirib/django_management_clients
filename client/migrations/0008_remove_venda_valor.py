# Generated by Django 2.0.1 on 2019-05-17 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_periodo_nome'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venda',
            name='valor',
        ),
    ]