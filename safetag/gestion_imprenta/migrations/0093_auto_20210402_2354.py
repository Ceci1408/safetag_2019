# Generated by Django 2.2.2 on 2021-04-02 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_imprenta', '0092_auto_20210402_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estado',
            name='estado',
            field=models.CharField(max_length=50),
        ),
    ]
