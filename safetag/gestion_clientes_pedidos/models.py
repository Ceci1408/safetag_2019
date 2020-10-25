from django.db import models
from django.forms import ModelForm
from django.core.exceptions import NON_FIELD_ERRORS

from gestion_imprenta.models import SolicitudPresupuesto, Cliente, Trabajo, Material, \
    ColorImpresion, Envio, Terminacion, MedidaEstandar


class SolicitudPresupuestoForm(ModelForm):
    class Meta:
        model = SolicitudPresupuesto
        fields = '__all__'
