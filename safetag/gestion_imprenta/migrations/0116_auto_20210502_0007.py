# Generated by Django 2.2.2 on 2021-05-02 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0115_auto_20210501_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarea',
            name='fecha_estimada_fin',
            field=models.DateField(),
        ),
    ]
