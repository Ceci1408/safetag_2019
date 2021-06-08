from django.forms import ModelForm, inlineformset_factory
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import *


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
    field_order = ['tipo_dato_contacto', 'dato_contacto_valor', 'contacto_horario',
                   'contacto_comentarios', 'flg_activo']

    class Meta:
        model = Contacto
        exclude = ['contacto_id', 'proveedor', 'servicio_tecnico', 'cliente','dato_contacto_flg_no_llame']
        labels = {
            'tipo_dato_contacto': _('Tipo'),
            'dato_contacto_valor': _('Dato de contacto'),
            'contacto_horario': _('Horario de contacto'),
            'contacto_comentarios': _('Comentarios'),
            'flg_activo': _('Dato activo')
        }
        widgets = {
            'contacto_comentarios': forms.Textarea(attrs={'rows': 5, 'cols': 15})
        }
        localized_fields = '__all__'


ClienteContactoInlineFormset = inlineformset_factory(
    Cliente,
    Contacto,
    extra=1,
    form=DatoContactoForm,
    can_delete=False
)


class DomicilioForm(ModelForm):
    field_order = ['tipo_domicilio', 'domicilio_calle', 'domicilio_altura', 'domicilio_depto', 'localidad', 'provincia', 'pais',
                   'flg_activo']

    class Meta:
        model = Domicilio
        localized_fields = '__all__'
        exclude = ['domicilio_id', 'proveedor', 'servicio_tecnico', 'cliente', 'fecha_carga','domicilio_latitud',
                   'domicilio_longitud', ]
        labels = {
            'tipo_domicilio': _('Tipo de Domicilio'),
            'domicilio_calle': _('Calle/Ruta'),
            'domicilio_altura': _('Altura/Km'),
            'domicilio_depto': _('Piso/Depto'),
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
    can_delete=False,
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
    can_delete=False,
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
    can_delete=False,
    form=DomicilioForm
)


class TrabajoForm(ModelForm):
    class Meta:
        model = Trabajo
        exclude = ['trabajo_id', 'fecha_carga', 'cantidades', 'terminaciones', ]
        labels = {
            'trabajo_descripcion': _('Nombre del Trabajo'),
            'autoadhesivo_flg': _('¿Es autoadhesivo?'),
            'doble_cara_flg': _('¿Admite doble faz?'),
            'tiempo_aprox_hs': _('Hs aprox'),
            'demasia_trabajo_mm': _('Demasía en mm'),
            'circular_flg': _('¿Es circular?'),
            'flg_activo': _('¿Está vigente?'),
            'medidas': _('Medidas que admite'),
            'materiales': _('Materiales que admite'),
            'maquinas_pliego': _('¿Con qué máquinas se puede realizar?')
        }
        localized_fields = '__all__'


class MedidaEstandarForm(ModelForm):
    class Meta:
        model = MedidaEstandar
        exclude = ['medida_estandar_id', 'fecha_carga']
        labels = {
            'medida_flg_circular': _('¿Es circular?'),
            'medida_1_cm': _('Medida 1 (cm)'),
            'medida_2_cm': _('Medida 2 (cm)'),
            'flg_activo': _('¿Medida vigente?')
        }
        localized_fields = '__all__'


class TrabajoCantidadesForm(ModelForm):
    class Meta:
        model = TrabajoCantidades
        exclude = ['fecha_carga']
        labels = {
            'descuento': _('Descuento (%)'),
            'flg_activo': _('¿Está vigente')
        }
        localized_fields = '__all__'


class TrabajoTerminacionesForm(ModelForm):
    class Meta:
        model = TrabajoTerminaciones
        exclude = ['fecha_carga']
        labels = {
            'terminacion': _('Terminación'),
            'flg_activo': _('¿Está vigente?')
        }
        localized_fields = '__all__'


TrabajoCantidadInlineFormset = inlineformset_factory(
    parent_model=Trabajo,
    model=TrabajoCantidades,
    form=TrabajoCantidadesForm,
    extra=5,
    max_num=10,
    validate_max=True,
    can_delete=False
)

TrabajoTerminacionInlineFormset = inlineformset_factory(
    parent_model=Trabajo,
    model=TrabajoTerminaciones,
    form=TrabajoTerminacionesForm,
    extra=3,
    max_num=5,
    validate_max=True,
    can_delete=True
)


class CantidadForm(ModelForm):
    class Meta:
        model = Cantidad
        exclude = ['cantidad_id', 'fecha_carga']
        labels = {
            'cantidad': _('Cantidad'),
            'flg_activo': _('¿Cantidad vigente?')
        }
        localized_fields = '__all__'





class MaterialForm(ModelForm):
    class Meta:
        model = Material
        exclude = ['material_id', 'fecha_carga']
        labels = {
            'material_descripcion': _('Material'),
            'material_alto_mm': _('Alto (mm)'),
            'material_ancho_mm': _('Ancho (mm)'),
            'material_costo_dolar': _('Costo (u$s)'),
            'material_gramaje_grs': _('Gramaje (grs)'),
            'material_demasia_hoja_mm': _('Demasía (mm)'),
            'material_proveedor': _('Proveedor'),
            'flg_activo': _('¿Material vigente?')
        }
        localized_fields = '__all__'


class MaquinaTerminacionForm(ModelForm):
    class Meta:
        model = MaquinaTerminacion
        exclude = ['maquina_id', 'fecha_carga', 'terminaciones']
        labels = {
            'maquina_marca': _('Marca'),
            'maquina_descripcion': _('Descripción'),
            'servicio_tecnico': _('Servicio Técnico'),
            'flg_activo': _('¿Está vigente?')
        }
        localized_fields = '__all__'


class MaquinaPliegoForm(ModelForm):
    class Meta:
        model = MaquinaPliego
        exclude = ['maquina_id', 'fecha_carga', 'colores_impresion']
        labels = {
            'maquina_marca': _('Marca'),
            'maquina_descripcion': _('Descripción'),
            'servicio_tecnico': _('Servicio Técnico'),
            'flg_activo': _('¿Está vigente?'),
            'maquina_pliego_ult_cambio_toner': _('Último cambio de tonner'),
            'demasia_impresion_mm': _('Demasía (mm)'),
            # 'colores_impresion': _('Colores')
        }
        localized_fields = '__all__'


class MaquinaPliegoColoresForm(ModelForm):
    class Meta:
        model = MaquinaPliegoColores
        exclude = ['maquina_pliego', 'fecha_carga']
        labels = {
            'color_impresion': _('Color'),
            'flg_activo': _('¿Está vigente?'),
            'costo_dolar': _('Costo (u$s)')
        }
        localized_fields = '__all__'


MaquinaPliegoColorInlineFormset = inlineformset_factory(
    MaquinaPliego,
    MaquinaPliegoColores,
    form=MaquinaPliegoColoresForm,
    extra=2,
    validate_max=True,
    can_delete=True
)


class EnvioForm(ModelForm):
    class Meta:
        model = Envio
        exclude = ['modo_envio_id', 'fecha_carga']
        labels = {
            'modo_envio': _('Tipo de envío'),
            'modo_envio_porc_adicional': _('Porcentaje adicional (%)'),
            'modo_envio_costo': _('Costo ($)'),
            'flg_activo': _('¿Está vigente?')
        }
        localized_fields = '__all__'


class EstadoForm(ModelForm):
    class Meta:
        model = Estado
        exclude = ['estado_id', 'fecha_carga']
        labels = {
            'estado': _('Estado'),
            'tipo_estado': _('Tipo'),
            'flg_activo': _('¿Está vigente?')
        }


class TipoTerminacionForm(ModelForm):
    class Meta:
        model = TipoTerminacion
        exclude = ['tipo_terminacion_id', 'fecha_carga']
        labels = {
            'tipo_terminacion': _('Tipo de terminación'),
            'flg_activo': _('¿Está vigente?')
        }
        localized_fields = '__all__'


class TerminacionForm(ModelForm):
    class Meta:
        model = Terminacion
        exclude = ['terminacion_id', 'fecha_carga']
        labels = {
            'terminacion': _('Terminación'),
            'flg_activo': _('¿Está vigente?'),
            'tipo_terminacion': _('Tipo de terminación')
        }
        localized_fields = '__all__'


class TerminacionMaquinaForm(ModelForm):
    class Meta:
        model = TerminacionesMaquinas
        exclude = ['fecha_carga', 'terminacion']
        labels = {
            'maquina_terminacion': _('Maquina de terminación'),
            'cant_hojas_max_permitidas': _('Cantidad máx de hojas'),
            'costo_dolar': _('Costo terminación (u$s)'),
            'flg_activo': _('¿Está vigente?')
        }

        localized_fields = '__all__'


TerminacionesMaquinasInlineFormset = inlineformset_factory(
    parent_model=Terminacion,
    model=TerminacionesMaquinas,
    form=TerminacionMaquinaForm,
    extra=2,
    can_delete=True
)


class SolicitudPresupuestoTerminacionesForm(ModelForm):
    class Meta:
        model = SolicitudPresupuestoTerminaciones
        exclude = ['solicitud']
        labels = {
            'terminacion': _('Terminación'),
            'doble_cara_flg': _('Doble Faz'),
            'maquina_terminacion': _('Maquina terminación'),
            'comentarios': _('Comentarios')
        }
        localized_fields = '__all__'


TerminacionesSolicitudInlineFormset = inlineformset_factory(
    parent_model=SolicitudPresupuesto,
    model=SolicitudPresupuestoTerminaciones,
    form=SolicitudPresupuestoTerminacionesForm,
    extra=0,
    can_delete=False
)


class SolicitudPresupuestoContactoForm(ModelForm):
    class Meta:
        model = SolicitudPresupuestoContactos
        exclude = ['solicitud', 'contacto','fecha_creacion']
        labels = {
            'flg_notificacion':_('Este contacto recibirá las notificaciones'),
            'flg_activo': _('Contacto activo para la solicitud'),
        }


class ComentariosForm(ModelForm):
    class Meta:
        model = Comentario
        exclude = ['solicitud', 'presupuesto', 'orden', 'fecha_comentario', 'usuario']
        labels = {
            'comentario': _('Comentario')
        }
        localized_fields = '__all__'


SolicitudComentariosInlineFormset = inlineformset_factory(
    parent_model=SolicitudPresupuesto,
    model=Comentario,
    form=ComentariosForm,
    extra=1,
    max_num=10,
    can_delete=True
)


class SolicitudPresupuestoForm(ModelForm):
    class Meta:
        model = SolicitudPresupuesto
        fields = ['maquina_pliego']
        labels = {
            'maquina_pliego': _('Máquina de impresión')
        }
        localized_fields = '__all__'


class PresupuestoForm(ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['margen_ganancia', 'cotizacion_dolar', 'costo_disenio']
        labels = {
            'margen_ganancia': _('Margen de ganancia (%)'),
            'costo_disenio': _('Costo de diseño'),
            'cotizacion_dolar': _('Cotización dolar')
        }
        localized_fields = '__all__'


SolicitudPresupuestoInlineFormset = inlineformset_factory(
    parent_model=SolicitudPresupuesto,
    model=Presupuesto,
    form=PresupuestoForm,
    extra=1
)


class PresupuestoEstadoForm(ModelForm):
    class Meta:
        model = PresupuestoEstado
        fields = ['estado']
        labels = {
            'estado': _('Nuevo estado')
        }
        localized_fields = '__all__'


class OrdenTrabajoEstadoForm(ModelForm):
    class Meta:
        model = OrdenTrabajoEstado
        fields = ['estado']
        labels = {
            'estado': _('Nuevo estado')
        }
        localized_fields = '__all__'


class TareaForm(ModelForm):
    class Meta:
        model = Tarea
        fields = ['tarea', 'fecha_estimada_fin', 'completa']
        labels = {
            'tarea': _('Tarea a crear'),
            'fecha_estimada_fin': _('Fecha estimada de finalización'),
            'completa': _('Tarea completa')
        }
        widgets={
            'fecha_estimada_fin': forms.SelectDateWidget()
        }
