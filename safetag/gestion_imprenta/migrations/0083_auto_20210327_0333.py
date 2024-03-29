# Generated by Django 2.2.2 on 2021-03-27 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0082_auto_20210327_0308'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='material',
            options={},
        ),
        migrations.AlterField(
            model_name='cantidad',
            name='flg_activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='colorimpresion',
            name='flg_activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='envio',
            name='flg_activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='estado',
            name='flg_activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='maquinapliego',
            name='flg_activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='maquinapliegocolores',
            name='flg_activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='maquinaterminacion',
            name='flg_activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='material',
            name='flg_activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='medidaestandar',
            name='flg_activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='serviciotecnico',
            name='flg_activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='subestado',
            name='flg_activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='terminacion',
            name='flg_activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='terminacionesmaquinas',
            name='flg_activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tipoterminacion',
            name='flg_activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='trabajocantidades',
            name='flg_activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='trabajoterminaciones',
            name='flg_activo',
            field=models.BooleanField(default=False),
        ),
    ]
