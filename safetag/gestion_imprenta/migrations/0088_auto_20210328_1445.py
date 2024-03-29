# Generated by Django 2.2.2 on 2021-03-28 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0087_presupuestoestado_fecha_cambio_estado'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comentario',
            options={'ordering': ['-fecha_comentario']},
        ),
        migrations.AlterField(
            model_name='trabajo',
            name='tiempo_aprox_hs',
            field=models.IntegerField(blank=True, help_text='Tiempo para realizar el trabajo (sin las terminaciones)', null=True),
        ),
        migrations.AlterModelTable(
            name='comentario',
            table='"comentarios"',
        ),
    ]
