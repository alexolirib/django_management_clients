# Generated by Django 2.0.1 on 2019-02-24 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_periodo'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodo',
            name='nome',
            field=models.CharField(max_length=60, null=True),
        ),
    ]
