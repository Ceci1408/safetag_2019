# Generated by Django 2.2.2 on 2021-03-25 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0073_auto_20210325_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='fecha_envio_presupuesto',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='presupuesto_comentarios_rechazo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]