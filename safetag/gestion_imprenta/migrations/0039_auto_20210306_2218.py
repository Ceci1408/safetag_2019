# Generated by Django 2.2.2 on 2021-03-06 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0038_auto_20210228_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trabajo',
            name='flg_activo',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
