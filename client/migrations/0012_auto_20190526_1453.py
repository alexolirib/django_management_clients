# Generated by Django 2.0.1 on 2019-05-26 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0011_auto_20190526_1248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itensdopedido',
            name='produto',
        ),
        migrations.RemoveField(
            model_name='itensdopedido',
            name='venda',
        ),
        migrations.RemoveField(
            model_name='venda',
            name='person',
        ),
        migrations.DeleteModel(
            name='ItensDoPedido',
        ),
        migrations.DeleteModel(
            name='Produto',
        ),
        migrations.DeleteModel(
            name='Venda',
        ),
    ]