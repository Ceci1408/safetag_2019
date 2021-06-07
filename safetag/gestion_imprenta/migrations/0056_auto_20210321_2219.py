# Generated by Django 2.2.2 on 2021-03-21 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0055_auto_20210314_2222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solicitudpresupuesto',
            old_name='solicitud_comentarios',
            new_name='solicitud_comentarios_cliente',
        ),
        migrations.AddField(
            model_name='solicitudpresupuesto',
            name='solicitud_comentarios_internos',
            field=models.TextField(blank=True, max_length=255),
        ),
    ]
