# Generated by Django 2.2.2 on 2021-03-24 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0067_presupuesto_presupuesto_costo_material'),
    ]

    operations = [
        migrations.RenameField(
            model_name='presupuesto',
            old_name='presupuesto_impresion',
            new_name='presupuesto_costo_impresion',
        ),
    ]