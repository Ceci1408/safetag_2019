# Generated by Django 2.2.2 on 2021-04-03 00:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0094_auto_20210402_2358'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='estado',
            name='unique_tipo_estado',
        ),
        migrations.AlterField(
            model_name='ordentrabajoestado',
            name='estado',
            field=models.ForeignKey(limit_choices_to={'entidad_asociada': 'orden_trabajo'}, on_delete=django.db.models.deletion.PROTECT, to='gestion_imprenta.Estado'),
        ),
        migrations.AlterField(
            model_name='presupuestoestado',
            name='estado',
            field=models.ForeignKey(limit_choices_to={'entidad_asociada': 'presupuesto'}, on_delete=django.db.models.deletion.PROTECT, to='gestion_imprenta.Estado'),
        ),
    ]
