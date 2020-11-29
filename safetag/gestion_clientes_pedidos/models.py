from django.db import models
from django.forms import ModelForm
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import gettext_lazy as _

from gestion_imprenta.models import SolicitudPresupuesto, Cliente, Trabajo, Material, \
    ColorImpresion, Envio, Terminacion, MedidaEstandar, SolicitudPresupuestoTerminaciones


class SolicitudPresupuestoForm(ModelForm):
    field_order = ['trabajo', 'material', 'color_impresion', 'medida_estandar', 'solicitud_orientacion',
                   'cantidad_estandar', 'solicitud_doble_cara_impresion_flg', 'solicitud_disenio_flg',
                   'solicitud_terminacion_flg', 'solicitud_adjunto_1', 'solicitud_adjunto_2', 'solicitud_adjunto_3',
                   'solicitud_express_flg', 'envio','solicitud_comentarios', 'solicitud_nombre', 'solicitud_apellido',
                   'soliciud_email']

    class Meta:
        model = SolicitudPresupuesto
        exclude = ['solicitud_email_enviado_flg',
                   'maquina_pliego_id',
                   'cantidad_hojas_estimadas',
                   ]

        labels = {
            'solicitud_disenio_flg': _('Requiere diseño'),
            'solicitud_comentarios': _('Comentarios adicionales'),
            'solicitud_terminacion_flg': _('Requiere terminaciones'),
            'solicitud_express_flg': _('Requiere prioridad (Express)'),
            'solicitud_doble_cara_impresion_flg': _('Requiere impresión doble faz'),
            'solicitud_adjunto_1': _('Suba su archivo (1)'),
            'solicitud_adjunto_2': _('Suba su archivo (2)'),
            'solicitud_adjunto_3': _('Suba su archivo (3)'),
            'solicitud_orientacion': _('Orientación del trabajo'),
            'trabajo': _('Seleccione el trabajo deseado'),
            'color_impresion': _('Seleccione el color de impresión'),
            'material': _('Seleccione el material'),
            'envio': _('Seleccione el método de envío'),
            'medida_estandar': _('Seleccione medida'),
            'cantidad_estandar': _('Seleccion la cantidad'),
            'solicitud_nombre': _('Nombre de quien solicita'),
            'solicitud_apellido': _('Apellido de quien solicita'),
            'solicitud_email': _('Email para enviar presupuesto')
        }

        localized_fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].queryset = Material.objects.none()
        self.fields['medida_estandar'].queryset = MedidaEstandar.objects.none()

        if 'trabajo' in self.data:
            try:
                trabajo_id = int(self.data.get('trabajo'))
                self.fields['material'].queryset = Material.objects.filter(trabajo_id=trabajo_id).order_by('material')
                self.fields['medida_estandar'].queryset = MedidaEstandar.objects.filter(trabajo_id=trabajo_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['material'].queryset = self.instance.trabajo.materiales_set.order_by('material')
            self.fields['medida_estandar'].queryset = self.instance.trabajo.medidas_set.order_by('medida_estandar_id')


class SolicitudPresupuestoTerminacionesForm(ModelForm):
    field_order = ['terminacion', 'doble_cara_flg']

    class Meta:
        model = SolicitudPresupuestoTerminaciones
        exclude = ['solicitud', 'maquina_terminacion']
        labels = {
            'terminacion': _('Seleccione terminación'),
            'doble_cara_flg': _('Requiere terminación doble faz')
        }
