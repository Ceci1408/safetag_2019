# Generated by Django 2.2.2 on 2021-02-15 00:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0033_auto_20210214_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='tipo_dato_contacto',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='gestion_imprenta.TipoContacto'),
        ),
    ]
