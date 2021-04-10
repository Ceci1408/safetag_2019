from django.forms import ModelForm, formset_factory, Select
from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import gettext_lazy as _

from gestion_imprenta.models import SolicitudPresupuesto, SolicitudPresupuestoTerminaciones, Material, Cantidad,\
    MedidaEstandar, Trabajo, Contacto, Cliente, ColorImpresion, Envio, Terminacion


class SolicitudPresupuestoForm(ModelForm):
    field_order = ['trabajo', 'material', 'color_impresion', 'medida_estandar', 'solicitud_orientacion',
                   'cantidad_estandar', 'solicitud_doble_cara_impresion_flg', 'solicitud_disenio_flg',
                   'solicitud_terminacion_flg',  'solicitud_adjunto_1', 'solicitud_adjunto_2', 'solicitud_adjunto_3',
                   'solicitud_express_flg', 'envio','solicitud_comentarios_cliente', 'doble_cara_flg' ]

    class Meta:
        model = SolicitudPresupuesto
        exclude = ['solicitud_email_enviado_flg',
                   'maquina_pliego',
                   'solicitud_terminaciones',
                   'contacto'
                   ]

        labels = {
            'solicitud_disenio_flg': _('Requiere diseño'),
            'solicitud_comentarios_cliente': _('Comentarios adicionales'),
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
            'cantidad_estandar': _('Seleccion la cantidad')
        }

        help_texts = {
            'solicitud_express_flg': _('Envío Express tiene costo adicional')
        }

        localized_fields = '__all__'


class SolicitudContactoForm(ModelForm):
    field_order = ['tipo_dato_contacto', 'dato_contacto_valor']
    prosp_nombre = forms.CharField(max_length=25, min_length=3, strip=True, label=_('Nombre'))
    prosp_apellido = forms.CharField(max_length=25, min_length=3, strip=True, label=_('Apellido'))

    class Meta:
        model = Contacto
        fields = ['tipo_dato_contacto', 'dato_contacto_valor']
        labels = {
            'tipo_dato_contacto': _('Tipo de contacto'),
            'dato_contacto_valor': _('Contacto')
        },
        localized_fields = '__all__'


SpContactoFormset = formset_factory(
    form=SolicitudContactoForm,
    extra=1,
    max_num=2
)


class SolicitudTerminacionesForm(ModelForm):
    field_order = ['terminacion', 'doble_cara_flg', 'comentarios']

    class Meta:
        model = SolicitudPresupuestoTerminaciones
        exclude = ['solicitud', 'maquina_terminacion']
        labels = {
            'terminacion': _('Terminacion'),
            'doble_cara_flg': _('Aplicar en ambas caras'),
            'comentarios': _('Comentarios'),
        }
        localized_fields = '__all__'
        widgets = {
            'terminacion': Select(attrs={'class': 'clase_terminacion'}),
        }


SpTerminacionesFormset = formset_factory(
    form=SolicitudTerminacionesForm,
    extra=2,
    max_num=3
)
