# Generated by Django 2.2.2 on 2021-03-25 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0070_auto_20210325_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='presupuesto_aceptado_flg',
            field=models.BooleanField(blank=True),
        ),
    ]