# Generated by Django 2.2.2 on 2021-05-23 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0127_auto_20210523_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trabajo',
            name='flg_activo',
            field=models.BooleanField(blank=True, default=False, editable=False),
        ),
    ]
