# Generated by Django 2.2.2 on 2021-04-02 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0090_auto_20210402_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='estado',
            name='entidad_asociada',
            field=models.CharField(choices=[('orden_trabajo', 'Orden de Trabajo'), ('presupuesto', 'Presupuesto')], default='orden_trabajo', max_length=50),
        ),
    ]
