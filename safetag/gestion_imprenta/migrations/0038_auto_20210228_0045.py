# Generated by Django 2.2.2 on 2021-02-28 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0037_auto_20210227_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='medidaestandar',
            name='medida_flg_circular',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trabajo',
            name='demasia_trabajo_mm',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Demasía sugerida para la impresión', max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='trabajo',
            name='tiempo_aprox_hs',
            field=models.IntegerField(blank=True, help_text='Tiempo para realizar el trabajo sin considerar las terminaciones', null=True),
        ),
    ]