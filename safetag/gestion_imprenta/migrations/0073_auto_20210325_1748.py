# Generated by Django 2.2.2 on 2021-03-25 17:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0072_auto_20210325_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='fecha_envio_presupuesto',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='presupuesto_aceptado_flg',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]