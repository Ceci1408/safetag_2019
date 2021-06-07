# Generated by Django 2.2.2 on 2021-03-26 21:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gestion_imprenta', '0080_remove_personal_tel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordentrabajoestado',
            name='personal',
        ),
        migrations.AddField(
            model_name='ordentrabajoestado',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Personal',
        ),
    ]