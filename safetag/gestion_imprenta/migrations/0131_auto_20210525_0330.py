# Generated by Django 2.2.2 on 2021-05-25 03:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0130_trabajoterminaciones_fecha_ultima_modificacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordentrabajo',
            name='fecha_ultimo_estado',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='estados',
            field=models.ManyToManyField(related_name='pres_historia_estados', through='gestion_imprenta.PresupuestoEstado', to='gestion_imprenta.Estado'),
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='fecha_ultimo_estado',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='ultimo_estado',
            field=models.ForeignKey(default=11, limit_choices_to={'entidad_asociada': 'presupuesto'}, on_delete=django.db.models.deletion.PROTECT, related_name='pres_ultimo_estado', to='gestion_imprenta.Estado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordentrabajo',
            name='ultimo_estado',
            field=models.ForeignKey(default=4, limit_choices_to={'entidad_asociada': 'orden_trabajo'},
                                    on_delete=django.db.models.deletion.PROTECT, related_name='ot_ultimo_estado',
                                    to='gestion_imprenta.Estado'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ordentrabajo',
            name='estados',
            field=models.ManyToManyField(related_name='ot_historia_estados', through='gestion_imprenta.OrdenTrabajoEstado', to='gestion_imprenta.Estado'),
        ),
    ]
