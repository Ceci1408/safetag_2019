# Generated by Django 2.2.2 on 2021-05-22 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0122_auto_20210512_0416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cliente_origen',
            field=models.CharField(choices=[('formulario_presupuesto', 'Formulario de Presupuesto'), ('manual', 'Manual')], default='manual', editable=False, max_length=25),
        ),
    ]
