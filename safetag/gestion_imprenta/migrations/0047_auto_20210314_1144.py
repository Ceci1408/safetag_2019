# Generated by Django 2.2.2 on 2021-03-14 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0046_auto_20210314_1142'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='trabajocantidades',
            name='unique_tipo_trabajo_cantidad',
        ),
        migrations.RenameField(
            model_name='trabajocantidades',
            old_name='tipo_trabajo',
            new_name='trabajo',
        ),
        migrations.AddConstraint(
            model_name='trabajocantidades',
            constraint=models.UniqueConstraint(fields=('trabajo', 'cantidad', 'descuento', 'flg_activo'), name='unique_trabajo_cantidad'),
        ),
        migrations.AlterModelTable(
            name='trabajocantidades',
            table='"trabajo_cantidades"',
        ),
    ]
