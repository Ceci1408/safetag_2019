# Generated by Django 2.2.2 on 2019-07-09 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0005_auto_20190709_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordentrabajo',
            name='solicitud',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='gestion_imprenta.SolicitudPresupuesto'),
        ),
    ]
