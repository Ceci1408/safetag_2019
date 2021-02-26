from django.forms import ModelForm, inlineformset_factory
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Cliente, Contacto, Domicilio, Proveedor, ServicioTecnico


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        exclude = ['cliente_id', 'cliente_fecha_alta']

        labels = {
            'cliente_nombre': _('Nombre'),
            'cliente_apellido': _('Apellido'),
            'cliente_email_contacto': _('Email')
        }
        localized_fields = '__all__'


class DatoContactoForm(ModelForm):
    field_order = ['tipo_dato_contacto', 'dato_contacto_valor', 'dato_contacto_flg_no_llame', 'contacto_horario',
                   'contacto_comentarios', 'flg_activo']

    class Meta:
        model = Contacto
        localized_fields = '__all__'
        exclude = ['contacto_id', 'proveedor', 'servicio_tecnico', 'cliente']
        labels = {
            'tipo_dato_contacto': _('Tipo'),
            'dato_contacto_valor': _('Dato de contacto'),
            'dato_contacto_flg_no_llame': _('No llame'),
            'contacto_horario': _('Horario de contacto'),
            'contacto_comentarios': _('Comentarios'),
            'flg_activo': _('Dato activo')
        }
        widgets = {
            'dato_contacto_flg_no_llame': forms.Select(choices=[
                ('si', 'Si'),
                ('no', 'No'),
                ('ns_nc', 'Desconoce')]),
            'contacto_comentarios': forms.Textarea(attrs={'rows':5, 'cols':15})
        }


ClienteContactoInlineFormset = inlineformset_factory(
    Cliente,
    Contacto,
    extra=3,
    form=DatoContactoForm
)


class DomicilioForm(ModelForm):
    field_order = ['tipo_domicilio','domicilio_calle', 'domicilio_altura', 'localidad', 'provincia', 'pais', 'domicilio_latitud',
                   'domicilio_longitud', 'flg_activo']

    class Meta:
        model = Domicilio
        localized_fields = '__all__'
        exclude = ['domicilio_id', 'proveedor', 'servicio_tecnico', 'cliente', 'fecha_carga']
        labels = {
            'tipo_domicilio': _('Tipo de Domicilio'),
            'domicilio_calle': _('Calle/Ruta'),
            'domicilio_altura': _('Altura/Km'),
            'localidad': _('Localidad'),
            'provincia': _('Provincia'),
            'pais': _('Pais'),
            'domicilio_latitud': _('Latitud'),
            'domicilio_longitud': _('Longitud'),
            'flg_activo': _('Activo')
        }


ClienteDomicilioInlineFormset = inlineformset_factory(
    Cliente,
    Domicilio,
    extra=2,
    can_delete=True,
    form=DomicilioForm
)


class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedor
        exclude = ['proveedor_id', 'fecha_carga']

        labels = {
            'proveedor_razon_social': _('Proveedor'),
            'proveedor_descripcion': _('Descripcion'),
            'nota_1': _('Notas'),
            'flg_activo': _('Activo')
        }
        localized_fields = '__all__'


ProveedorContactoInlineFormset = inlineformset_factory(
    Proveedor,
    Contacto,
    extra=3,
    form=DatoContactoForm
)


ProveedorDomicilioInlineFormset = inlineformset_factory(
    Proveedor,
    Domicilio,
    extra=2,
    can_delete=True,
    form=DomicilioForm
)


class ServicioTecnicoForm(ModelForm):
    class Meta:
        model = ServicioTecnico
        exclude = ['servicio_tecnico_id', 'fecha_carga']

        labels = {
            'servicio_tecnico': _('Servicio Técnico'),
            'flg_activo': _('Activo')
        }
        localized_fields = '__all__'


ServicioTecnicoContactoInlineFormset = inlineformset_factory(
    ServicioTecnico,
    Contacto,
    extra=3,
    form=DatoContactoForm
)

ServicioTecnicoDomicilioInlineFormset = inlineformset_factory(
    ServicioTecnico,
    Domicilio,
    extra=2,
    can_delete=True,
    form=DomicilioForm
)