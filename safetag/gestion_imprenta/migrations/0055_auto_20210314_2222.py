# Generated by Django 2.2.2 on 2021-03-14 22:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0054_auto_20210314_2106'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='colorimpresion',
            name='unique_color_impresion',
        ),
        migrations.AddField(
            model_name='colorimpresion',
            name='fecha_carga',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='colorimpresion',
            name='flg_activo',
            field=models.BooleanField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='colorimpresion',
            constraint=models.UniqueConstraint(fields=('color_impresion', 'flg_activo'), name='unique_color_impresion'),
        ),
    ]
