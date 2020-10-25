from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.conf import settings
from django.forms.models import inlineformset_factory, modelformset_factory
from django.utils.translation import gettext_lazy as _
import re
import random


class Cliente(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    cliente_nombre = models.CharField(max_length=100, blank=False, null=False)
    cliente_apellido = models.CharField(max_length=100, blank=False, null=False)
    cliente_fecha_alta = models.DateTimeField(auto_now_add=True)
    cliente_email_contacto = models.EmailField(blank=False)

    class Meta:
        db_table = '"cliente"'
        ordering = ['cliente_id']
        indexes = [
            models.Index(fields=['cliente_nombre', 'cliente_apellido'], name='nombre_apellido_idx'),
            models.Index(fields=['cliente_nombre'], name='nombre_idx'),
            models.Index(fields=['cliente_email_contacto'], name='email_idx')
        ]
        constraints = [
            models.UniqueConstraint(fields=['cliente_email_contacto'], name='unique_email'),
        ]

    def clean(self):
        if not self.cliente_nombre.isalpha():
            raise ValidationError({'cliente_nombre': _('Sólo se permiten letras')})

        if not self.cliente_apellido.isalpha():
            raise ValidationError({'cliente_apellido': _('Sólo se permiten letras')})


# TODO hacer obligatorios localidad, provincia y pais. Para hacer geolocalización
class TipoDomicilio(models.Model):
    tipo_domicilio_id = models.AutoField(primary_key=True),
    tipo_domicilio_descripcion = models.CharField(max_length=25, blank=False, null=True)

    class Meta:
        db_table = '"tipo_domicilio"'
        constraints = [
            models.UniqueConstraint(
                fields=['tipo_domicilio_descripcion'], name='unique_tipo_domicilio'),
        ]


class Domicilio(models.Model):
    domicilio_id = models.AutoField(primary_key=True)
    domicilio_calle = models.CharField(max_length=100, blank=False)
    domicilio_altura = models.PositiveIntegerField()
    domicilio_latitud = models.DecimalField(max_digits=12, decimal_places=10, blank=True, null=True)
    domicilio_longitud = models.DecimalField(max_digits=12, decimal_places=10, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=False)
    provincia = models.CharField(max_length=100, blank=False)
    localidad = models.CharField(max_length=100, blank=False)
    cliente = models.ForeignKey(Cliente, models.PROTECT, blank=True, null=True)
    proveedor = models.ForeignKey('Proveedor', models.PROTECT, blank=True, null=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)
    servicio_tecnico = models.ForeignKey('ServicioTecnico', models.PROTECT, blank=True, null=True)

    class Meta:
        db_table = '"domicilio"'
        indexes = [
            models.Index(fields=['domicilio_calle', 'domicilio_altura'], name='calle_altura_idx')
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['cliente', 'domicilio_calle', 'domicilio_altura', 'localidad', 'provincia','pais'],
                name='unique_domicilio_cliente'),
            models.UniqueConstraint(
                fields=['proveedor', 'domicilio_calle', 'domicilio_altura', 'localidad', 'provincia','pais'],
                name='unique_domicilio_proveedor')
        ]

    def clean(self):
        if not self.pais.isalpha():
            raise ValidationError({'tipo_contacto_desc': _('Sólo se permiten letras')})
        if not self.provincia.isalpha():
            raise ValidationError({'tipo_contacto_desc': _('Sólo se permiten letras')})


class TipoContacto(models.Model):
    tipo_contacto_id = models.AutoField(primary_key=True)
    tipo_contacto_desc = models.CharField(max_length=25, blank=False, null=False)

    class Meta:
        db_table = '"tipo_contacto"'
        constraints = [
            models.UniqueConstraint(
                fields=['tipo_contacto_desc'], name='tipo_conacto_unique')]

    def clean(self):
        if not self.tipo_contacto_desc.isalpha():
            raise ValidationError({'tipo_contacto_desc': _('Sólo se permiten letras')})


class Contacto(models.Model):
    contacto_id = models.AutoField(primary_key=True)
    contacto_horario = models.CharField(max_length=100, blank=True, null=False)
    contacto_comentarios = models.TextField(blank=True, null=True)
    dato_contacto_valor = models.CharField(max_length=50)
    tipo_dato_contacto = models.ForeignKey(to=TipoContacto, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE, blank=True, null=True)
    servicio_tecnico = models.ForeignKey('ServicioTecnico', on_delete=models.CASCADE, blank=True, null=True)
    dato_contacto_flg_no_llame = models.NullBooleanField()
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        db_table = '"contacto"'
        indexes = [
            models.Index(fields=['dato_contacto_valor', 'tipo_dato_contacto'], name='tipo_dato_contacto_idx')
        ]
        constraints = [
            models.UniqueConstraint(fields=['dato_contacto_valor', 'tipo_dato_contacto', 'cliente'],
                                    name='unique_dc_cliente'),
            models.UniqueConstraint(fields=['dato_contacto_valor', 'tipo_dato_contacto', 'proveedor'],
                                    name='unique_dc_proveedor'),
            models.UniqueConstraint(fields=['dato_contacto_valor', 'tipo_dato_contacto', 'servicio_tecnico'],
                                    name='unique_dc_service'),
        ]

    def clean(self):
        pattern = '[^@]+@[^@]+\.[^@]+'

        if self.dato_contacto_valor is not None:
            result = re.match(pattern, self.dato_contacto_valor)

            if self.tipo_dato_contacto == 'EMAIL' and not result:
                raise ValidationError({'dato_contacto_valor': _('El dato de contacto no tiene el formato necesario')})

            if self.tipo_dato_contacto == 'EMAIL' and result and self.dato_contacto_flg_no_llame is not None:
                raise ValidationError({'dato_contacto_flg_no_llame': _('No use el flag. Aplica sólo para teléfonos')})

            if self.tipo_dato_contacto in ('CEL', 'TEL') and not self.dato_contacto_valor.isdigit():
                raise ValidationError({'dato_contacto_valor': _('El dato de contacto no tiene el formato necesario')})

            #TODO este no se si sea necesario
            if self.tipo_dato_contacto in ('CEL', 'TEL') and self.dato_contacto_valor.isdigit() and len(self.dato_contacto_valor) != 10:
                raise ValidationError({'dato_contacto_valor': _('El dato de contacto no tiene los dígitos correctos. Ingrese sin el cero. ')})


class Proveedor(models.Model):
    proveedor_id = models.AutoField(primary_key=True)
    proveedor_razon_social = models.CharField(max_length=100)
    proveedor_descripcion = models.CharField(max_length=200, blank=True, null=True)
    nota_1 = models.TextField(blank=True, null=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        db_table = '"proveedor"'
        indexes = [
            models.Index(fields=['proveedor_razon_social'], name='proveedor_rs_idx')
        ]
        constraints = [
             models.UniqueConstraint(fields=['proveedor_razon_social'], name='unique_proveedor'),
         ]


class Material(models.Model):
    material_id = models.AutoField(primary_key=True)
    material_descripcion = models.CharField(max_length=100, blank=False, null=False)
    material_alto_mm = models.IntegerField(blank=False, null=False )
    material_ancho_mm = models.IntegerField(blank=False, null=False)
    material_costo_dolar = models.DecimalField(max_digits=10, decimal_places=3, blank=False, null=False)
    material_gramaje_grs = models.IntegerField(blank=True, null=True)
    material_demasia_hoja_mm = models.DecimalField(max_digits=10, decimal_places=2,  blank=False, null=False)
    material_proveedor = models.ManyToManyField(Proveedor)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    def clean(self):
        if any(p.isdigit() for p in self.material):
            raise ValidationError({'material': _('Sólo se permiten letras')})

    class Meta:
        db_table = '"material"'
        indexes = [
            models.Index(fields=['material_descripcion'], name='material_desc_idx')
        ]
        constraints = [
            models.UniqueConstraint(fields=['material_descripcion', 'material_alto_mm', 'material_ancho_mm', 'material_gramaje_grs'], name='unique_material'),
        ]


class TipoTerminacion(models.Model):
    tipo_terminacion_id = models.AutoField(primary_key=True)
    tipo_terminacion = models.CharField(max_length=25, blank=False, null=False, unique=True,
                                        error_messages = {'unique': _('Esta terminación ya existe')})

    class Meta:
        db_table = '"tipo_terminacion"'
        constraints = [
            models.UniqueConstraint(fields=['tipo_terminacion'], name='unique_tipo_terminacion'),
        ]

    def clean(self):
        if any(tt.isdigit() for tt in self.tipo_terminacion):
            raise ValidationError({'tipo_terminacion': _('Sólo se permiten letras')})


class Terminacion(models.Model):
    terminacion_id = models.AutoField(primary_key=True)
    terminacion = models.CharField(max_length=100, blank=False, null=False, unique=True,
                                   error_messages={'unique': _('Esta terminación ya existe')})
    tipo_terminacion = models.ForeignKey(to=TipoTerminacion, on_delete=models.PROTECT)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        db_table = '"terminacion"'
        constraints = [
            models.UniqueConstraint(fields=['terminacion'], name='unique_terminacion'),
        ]
        indexes = [
            models.Index(fields=['terminacion'], name='terminacion_idx')
        ]

    def clean(self):
        if any(tt.isdigit() for tt in self.terminacion):
            raise ValidationError({'terminacion': _('Sólo se permiten letras')})


class Trabajo(models.Model):
    trabajo_id = models.AutoField(primary_key=True)
    trabajo_descripcion = models.CharField(max_length=50, unique=True, error_messages={'unique': _('Este tipo de trabajo ya existe')})
    autoadhesivo_flg = models.BooleanField(blank=False, null=False)
    doble_cara_flg = models.BooleanField(blank=False, null=False)
    tiempo_aprox_hs = models.IntegerField(blank=True, null=True)
    demasia_trabajo_mm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    circular_flg = models.BooleanField(blank=False, null=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)
    medidas = models.ManyToManyField('MedidaEstandar')
    cantidades = models.ManyToManyField('Cantidad', through='TrabajoCantidades')
    terminaciones = models.ManyToManyField(Terminacion),
    materiales = models.ManyToManyField(Material)
    maquinas_pliego = models.ManyToManyField('MaquinaPliego')


    class Meta:
        db_table = '"tipo_trabajo"'


    def clean(self):
        if any(tt.isdigit() for tt in self.tipo_trabajo):
            raise ValidationError({'tipo_trabajo': _('Sólo se permiten letras')})

        if self.tipo_trabajo_autoadhesivo_flg and self.tipo_trabajo_doble_cara_flg:
            raise ValidationError({'tipo_trabajo_doble_cara_flg': _('Si el trabajo es autoadhesivo, no permite impresión doble cara')})

    def __str__(self):
        return self.trabajo_descripcion


class MedidaEstandar(models.Model):
    medida_estandar_id = models.AutoField(primary_key=True)
    medida_1_cm = models.DecimalField(max_digits=10, decimal_places=2)
    medida_2_cm = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        db_table = 'medida_estandar'
        constraints = [
            models.UniqueConstraint(fields=['medida_1_cm', 'medida_2_cm'],
                                    name='unique_medida_estandar'),
        ]
        ordering = ['medida_1_cm', 'medida_2_cm']

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and (unique_check == ('medida_1_cm', 'medida_2_cm')
                                          or unique_check == ('medida_2_cm', 'medida_1_cm')):
            return 'Esta combinación ya existe'
        else:
            return super(MedidaEstandar, self).unique_error_message(model_class, unique_check)

    def __str__(self):
        return str(self.medida_1_cm) if self.medida_2_cm == 0 else str(self.medida_1_cm)+' x '+str(self.medida_2_cm)


class Cantidad(models.Model):
    cantidad_id = models.AutoField(primary_key=True)
    cantidad = models.IntegerField(blank=False, null=False, unique=True,
                                   error_messages={'unique':'Esta cantidad ya existe'})
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    def __str__(self):
        return str(self.cantidad)

    class Meta:
        db_table='"cantidad"'
        ordering = ['cantidad']
        constraints = [
            models.UniqueConstraint(fields=['cantidad'], name='unique_cantidad'),
        ]


class TrabajoCantidades(models.Model):
    tipo_trabajo = models.ForeignKey(Trabajo, on_delete=models.PROTECT)
    cantidad = models.ForeignKey(Cantidad, on_delete=models.PROTECT)
    descuento = models.PositiveSmallIntegerField(blank=True, null=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        db_table='"trabajo_cantidades"'
        constraints = [
            models.UniqueConstraint(fields=['tipo_trabajo', 'cantidad', 'descuento', 'flg_activo'],
                                    name='unique_tipo_trabajo_cantidad'),
        ]


class ColorImpresion(models.Model):
    color_impresion_id = models.AutoField(primary_key=True)
    color_impresion = models.CharField(max_length=50, null=False, blank=False, unique=True, \
                                       error_messages={'unique': _('Este color de impresión ya existe')})

    class Meta:
        db_table='"color_impresion"'
        constraints = [
            models.UniqueConstraint(fields=['color_impresion'], name='unique_color_impresion'),
        ]

    def clean(self):
        if not self.color_impresion.isalpha():
            raise ValidationError({'color_impresion': _('Sólo se permiten letras')})

    def __str__(self):
        return self.color_impresion


class Maquina(models.Model):
    maquina_id = models.AutoField(primary_key=True)
    maquina_marca = models.CharField(max_length=50, blank=True, null=True)
    maquina_descripcion = models.CharField(max_length=100, blank=True, null=True)
    servicio_tecnico = models.ForeignKey('ServicioTecnico', on_delete=models.PROTECT, blank=True, null=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        abstract = True
        ordering = ['maquina_id']

    def __str__(self):
        return "{} - {} ".format(self.maquina_marca, self.maquina_descripcion)


class MaquinaTerminacion(Maquina):
    terminaciones = models.ManyToManyField(Terminacion, through='TerminacionesMaquinas')

    class Meta(Maquina.Meta):
        db_table = '"maquina_terminacion"'


class TerminacionesMaquinas(models.Model):
    maquina_terminacion = models.ForeignKey(MaquinaTerminacion, on_delete=models.PROTECT)
    terminacion = models.ForeignKey(Terminacion, on_delete=models.PROTECT)
    cant_hojas_max_permitidas = models.PositiveSmallIntegerField(blank=True, null=False, default=0)
    costo_dolar = models.DecimalField(max_digits=5, decimal_places=3, blank=False, null=False)

    class Meta:
        db_table = '"terminaciones_maquinas"'
        constraints = [
            models.UniqueConstraint(fields=['maquina_terminacion', 'terminacion'],
                                    name='unique_maq_terminacion_terminaciones'),
        ]


class MaquinaPliego(Maquina):
    maquina_pliego_ult_cambio_toner = models.DateField(auto_now=True, null=True)
    demasia_impresion_mm = models.PositiveSmallIntegerField(blank=False, null=False)
    colores_impresion = models.ManyToManyField(ColorImpresion, through='MaquinaPliegoColores')

    class Meta(Maquina.Meta):
        db_table = '"maquina_pliego"'
        constraints = [
            models.UniqueConstraint(fields=['maquina_id', 'fecha_carga', 'flg_activo'], name='unique_maq_pliego'),
        ]


class MaquinaPliegoColores(models.Model):
    maquina_pliego = models.ForeignKey(MaquinaPliego, on_delete=models.PROTECT)
    color_impresion = models.ForeignKey(ColorImpresion, on_delete=models.PROTECT)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)
    costo_dolar = models.DecimalField(max_digits=5, decimal_places=3, blank=False, null=False)

    class Meta:
        db_table ='"maquina_pliego_colores"'
        constraints = [
            models.UniqueConstraint(fields=['maquina_pliego', 'color_impresion', 'fecha_carga', 'flg_activo'],
                                    name='unique_pliego_color'),
        ]



class ServicioTecnico(models.Model):
    servicio_tecnico_id = models.AutoField(primary_key=True)
    servicio_tecnico = models.CharField(max_length=100, blank=False, null=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        db_table = '"servicio_tecnico"'
        constraints = [
            models.UniqueConstraint(fields=['servicio_tecnico'], name='unique_service'),
        ]

    def clean(self):
        if not self.servicio_tecnico.isalpha():
            raise ValidationError({'servicio_tecnico': _('Sólo se permiten letras')})


class PagoRecibido(models.Model):
    TIPO_PAGO = (
        ('1', 'Efectivo'),
        ('2', 'Transferencia Bancaria'),
        ('3', 'Cheque'),
        ('4', 'Mercado Pago')
    )

    pago_recibido_id = models.AutoField(primary_key=True)
    pego_recibido_tipo = models.CharField(choices=TIPO_PAGO, max_length=5, blank=True, null=True)
    pago_recibido_fecha_cobro = models.DateTimeField(auto_now_add=True)
    pago_recibido_monto_cobro = models.DecimalField(max_digits=6, decimal_places=2, blank=False, null=False)
    presupuesto = models.ForeignKey('Presupuesto', on_delete=models.PROTECT)

    class Meta:
        db_table = '"pago_recibido"'
        ordering = ['-pago_recibido_fecha_cobro', 'presupuesto']
        indexes = [
            models.Index(fields=['pago_recibido_fecha_cobro', 'presupuesto'])
        ]


class Envio(models.Model):
    ENVIO = (
        ('moto', 'Envío por moto'),
        ('retiro_local', 'Retiro por local'),
        ('correo', 'Envío por correo')
    )
    modo_envio_id = models.AutoField(primary_key=True)
    modo_envio = models.CharField(choices=ENVIO, max_length=20, blank=False, null=False, unique=True)
    modo_envio_porc_adicional = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    modo_envio_costo = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, default=0)

    class Meta:
        db_table = '"envio"'

    def __str__(self):
        return self.modo_envio

# TODO Chequear el tema de los adjuntos
class SolicitudPresupuesto(models.Model):
    ORIENTACION = (
        ('V', 'Vertical'),
        ('H', 'Horizontal')
    )
    solicitud_id = models.AutoField(primary_key=True)
    solicitud_fecha = models.DateTimeField(auto_now_add=True)
    solicitud_disenio_flg = models.BooleanField()
    solicitud_comentarios = models.TextField(max_length=255)
    solicitud_terminacion_flg = models.BooleanField()
    solicitud_express_flg = models.BooleanField()
    solicitud_doble_cara_impresion_flg = models.BooleanField()
    solicitud_adjunto_1 = models.FileField(blank=True, null=True)
    solicitud_adjunto_2 = models.FileField(blank=True, null=True)
    solicitud_adjunto_3 = models.FileField(blank=True, null=True)
    solicitud_orientacion = models.CharField(choices=ORIENTACION, max_length=5, blank=True, null=True)
    solicitud_email_enviado_flg = models.BooleanField(default=False)
    trabajo = models.ForeignKey(Trabajo, on_delete=models.PROTECT, null=False)
    color_impresion = models.ForeignKey(ColorImpresion, on_delete=models.PROTECT, null=False)
    material = models.ForeignKey(Material, on_delete=models.PROTECT, null=False)
    envio = models.ForeignKey(Envio, on_delete=models.PROTECT, null=False)
    medida_estandar = models.ForeignKey(MedidaEstandar, on_delete=models.PROTECT, null=False)
    cantidad_estandar = models.ForeignKey(Cantidad, on_delete=models.PROTECT, null=False)
    cantidad_hojas_estimadas = models.SmallIntegerField()
    maquina_pliego_id = models.ForeignKey(MaquinaPliego, on_delete=models.PROTECT, blank=True, null=True)
    solicitud_nombre = models.CharField(max_length=25, blank=False, null=False)
    solicitud_apellido = models.CharField(max_length=25, blank=False, null=False)
    solicitud_email = models.EmailField(max_length=25, blank=False, null=False)

    class Meta:
        db_table = '"solicitud_presupuesto"'

    def clean(self):
        if self.trabajo.autoadhesivo_flg and self.solicitud_doble_cara_impresion_flg:
            raise ValidationError({'solicitud_doble_cara_impresion_flg': _('El tipo de trabajo es autoadhesivo y '
                                                                           'no se puede hacer impresión en ambas caras')})
        if not self.solicitud_apellido.isalpha():
            raise ValidationError({'solicitud_apellido': _('Sólo se permiten letras')})

        if not self.solicitud_nombre.isalpha():
            raise ValidationError({'solicitud_nombre': _('Sólo se permiten letras')})



class SolicitudPresupuestoTerminaciones(models.Model):
    solicitud = models.ForeignKey(SolicitudPresupuesto, on_delete=models.PROTECT)
    terminacion = models.ForeignKey(Terminacion, on_delete=models.PROTECT)
    doble_cara_flg = models.BooleanField()
    maquina_terminacion = models.ForeignKey(MaquinaTerminacion, on_delete=models.PROTECT)

    class Meta:
        db_table = '"solicitud_terminaciones"'
        constraints = [
            models.UniqueConstraint(fields=['solicitud', 'terminacion', 'maquina_terminacion'],
                                    name='unique_solicitud_terminaciones'),
        ]


class Presupuesto(models.Model):
    solicitud = models.ForeignKey(SolicitudPresupuesto, on_delete=models.PROTECT)
    presupuesto_porc_ganancia = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    presupuesto_hojas_utilizadas = models.IntegerField(blank=False, null=False)
    presupuesto_precio_dolar = models.DecimalField(max_digits=5, decimal_places=3, blank=False, null=False)
    presupuesto_costo_materiales = models.DecimalField(max_digits=6, decimal_places=3, blank=False, null=False)
    presupuesto_costo_disenio = models.DecimalField(max_digits=6, decimal_places=3, blank=False, null=False)
    presupuesto_costo_unitario = models.DecimalField(max_digits=6, decimal_places=3, blank=False, null=False)
    presupuesto_precio_cliente = models.DecimalField(max_digits=6, decimal_places=3, blank=False, null=False)
    presupuesto_costo_terminaciones = models.DecimalField(max_digits=6, decimal_places=3, blank=False, null=False)
    fecha_carga = fecha_carga = models.DateTimeField(auto_now_add=True)
    presupuesto_cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)

    class Meta:
        db_table='"presupuesto"'
        ordering = ['fecha_carga']

    def clean(self):
        if not self.solicitud.solicitud_disenio_flg and self.presupuesto_costo_disenio is not None:
            raise ValidationError({'presupuesto_costo_disenio': _('La solicitud no incluía diseño')})


class Estado(models.Model):
    TIPO_ESTADO = (
        ('Final', 'Estado final'),
        ('Intermedio', 'Estado intermedio'),
        ('Inicial', 'Estado inicial')
    )
    estado_id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=50, blank=False, null=False, unique=True,
                              error_messages={'unique': _('Este estado ya está registrado')})
    tipo_estado = models.CharField(choices=TIPO_ESTADO, max_length=50, null=False, blank=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        db_table='"estado"'
        constraints = [
            models.UniqueConstraint(fields=['estado', 'tipo_estado'],
                                    name='unique_tipo_estado'),
        ]


class OrdenTrabajo(models.Model):
    orden_id = models.AutoField(primary_key=True)
    presupuesto = models.OneToOneField(Presupuesto, on_delete=models.PROTECT, blank=True, null=True)
    orden_fecha_creacion = models.DateTimeField(auto_now_add=True)
    orden_impresion_realizada_flg = models.BooleanField()
    orden_terminacion_realizada_flg = models.BooleanField()
    orden_disenio_realizado_flg = models.BooleanField()
    orden_comentarios = models.TextField()
    estados = models.ManyToManyField(Estado, through='OrdenTrabajoEstado')

    class Meta:
        db_table ='"orden_trabajo"'
        ordering = ['orden_fecha_creacion']


class OrdenTrabajoEstado(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_cambio_estado = models.DateTimeField(auto_now_add=True)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    orden_trabajo = models.ForeignKey(OrdenTrabajo, on_delete=models.PROTECT)
    personal = models.ForeignKey('Personal', on_delete=models.PROTECT)

    class Meta:
        db_table = '"orden_trabajo_estados"'
        ordering = ['orden_trabajo', 'estado']


class Personal(models.Model):
    TIPO_DOC = (
        ('DNI', 'DNI'),
        ('CUIL', 'CUIL'),
        ('LC', 'LC'),
        ('LE', 'LE'),
        ('CUIT', 'CUIT'),
        ('PASA', 'PASAPORTE')
    )
    #user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_column='user_id', related_name='%(class)s_requests_created')
    user_id = models.OneToOneField(User, on_delete=models.PROTECT, db_column='user_id', related_name='personal')
    tel = models.CharField(max_length=20, blank=True, null=True)
    cel = models.CharField(max_length=20, blank=True, null=True)
    confirmado = models.BooleanField(default=False)
    tipo_documento = models.CharField(choices=TIPO_DOC, max_length=10, blank=False, null=False)
    numero_documento = models.CharField(max_length=12, blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tipo_documento', 'numero_documento'], name='unique_tipo_nro_doc_personal'),
        ]


''' 
##########################################
    Acá van los formularios
##########################################
'''

'''
class TipoClienteForm(ModelForm):
    class Meta:
        model = TipoCliente
        exclude = ['tipo_cliente_id', 'fecha_carga']
        error_message = {
                            NON_FIELD_ERRORS: {
                                'unique_together': "%(field_labels)s del modelo %(model_name)s  no %(es)son %(único)s.",
                            }
                        },





class ClientePublicoForm(ModelForm):
    class Meta:
        model = Cliente
        exclude = ['cliente_id', 'cliente_ml_email', 'cliente_original_lista_dist', 'cliente_fecha_alta',
                   'cliente_fecha_activo', 'cliente_flg_autenticado', 'tipo_cliente' ]

        error_message = {
                            NON_FIELD_ERRORS: {
                                'unique_together': "%(field_labels)s del modelo %(model_name)s  no %(es)son %(único)s.",
                            }
                        },

class DomicilioForm(ModelForm):
    class Meta:
        model = Domicilio
        exclude = ['domicilio_id', 'cliente', 'proveedor', 'fecha_carga', 'domicilio_longitud',
                   'domicilio_latitud', ]
        labels = {
            'domicilio_calle': _('Calle'),
            'domicilio_entre_calle_1': _('Entre calle (1)'),
            'domicilio_entre_calle_2': _('Entre calle (2)'),
            'domicilio_entre_calle_3': _('Entre calle (3)'),
            'domicilio_altura': _('Altura'),
            'flg_activo': _('Domicilio Activo')
        }
        error_message = {
                            NON_FIELD_ERRORS: {
                                'unique_together': "%(field_labels)s del modelo %(model_name)s  no %(es)son %(único)s.",
                            }
                        },

# TODO Este formulario si y sólo si debe llamarse cuando exista una instancia de Cliente, proveedor o Servicio Tecnico.
class ContactoForm(ModelForm):
    class Meta:
        model = Contacto
        exclude = ['dato_contacto_id', 'cliente', 'proveedor', 'servicio_tecnico', 'fecha_carga']
        labels = {
            'flg_activo': _('Activo'),
            'dato_contacto_valor':_('Dato (email/celular/teléfono'),
            'tipo_dato_contacto': _('Tipo dato de contacto'),
            'dato_contacto_interno': _('Interno'),
            'dato_contacto_uso': _('Uso'),
            'dato_contacto_horario_contacto': _('Horario de contacto'),
            'dato_contacto_flg_no_llame': _('Registro No Llame'),
            'dato_contacto_comentarios': _('Comentarios'),
        }
    field_order = ['dato_contacto_uso', 'tipo_dato_contacto', 'dato_contacto_valor', 'dato_contacto_interno',
                   'dato_contacto_horario_contacto', 'dato_contacto_flg_no_llame', 'dato_contacto_comentarios',
                   'flg_activo']


class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedor
        exclude = ['proveedor_id', 'fecha_carga']
        labels = {
            'proveedor_razon_social': _('Razón Social'),
            'proveedor_tipo_doc': _('Tipo documento'),
            'proveedor_nro_doc': _('Nro documento'),
            'proveedor_descripción': _('Descripción'),
            'nota_1': _('Notas'),
            'flg_activo': _('Activo')
        }


class MaterialForm(ModelForm):
    class Meta:
        model = Material
        exclude = ['material_id', 'fecha_carga']
        labels = {
            'material_alto_mm': _('Alto  (mm)'),
            'material_ancho_mm': _('Ancho (mm)'),
            'material_costo_dolar': _('Costo (u$s)'),
            'material_gramaje_grs': _('Gramaje'),
            'material_demasia_hoja_mm': _('Demasía (mm)'),
            'flg_activo': _('Activo')
        }
        widgets = {
            'proveedores': forms.SelectMultiple(),
            'trabajos': forms.SelectMultiple()
        }


class TipoTrabajoForm(ModelForm):
    class Meta:
        model = TipoTrabajo
        exclude = ['tipo_trabajo_id', 'fecha_carga', 'cantidades']
        labels = {
            'tipo_trabajo': _('Trabajo'),
            'tipo_trabajo_autoadhesivo_flg': _('Es autoadhesivo'),
            'tipo_trabajo_doble_cara_flg': _('Permite impresión doble cara'),
            'tipo_trabajo_tiempo_aprox_hs': _('Tiempo de realización aprox (Hs)'),
            'tipo_trabajo_demasia_trabajo_mm': _('Demasía aprox (mm)'),
            'tipo_trabajo_circular_flg': _('Es circular'),
            'flg_activo': _('Trabajo activo')
        }
        widgets = {
            'medidas': forms.SelectMultiple(),
            #'cantidades': forms.SelectMultiple(),
            'terminaciones': forms.SelectMultiple(),
            'materiales': forms.SelectMultiple()
        }
        help_texts={
            'medidas': _('Mantenga <Ctrl> presionado para seleccionar más de una opción'),
            'materiales': _('Mantenga <Ctrl> presionado para seleccionar más de una opción'),
        }


class MedidaEstandarForm(ModelForm):
    class Meta:
        model = MedidaEstandar
        exclude = ['medida_estandar_id', 'fecha_carga']
        labels = {
            'medida_1_cm': _('Medida 1 (cm)'),
            'medida_2_cm': _('Medida 2 (cm)'),
            'flg_activo': _('Medida activa')
        }
        error_messages = {
             NON_FIELD_ERRORS: {
                 'unique_together': "%(field_labels)s del modelo %(model_name)s  no son únicos.",
             }
         }


class CantidadForm(ModelForm):
    class Meta:
        model = Cantidad
        exclude = ['cantidad_id', 'fecha_carga']
        labels = {
            'flg_activo': _('Cantidad activa')
        }


class TipoTrabajoCantidadesForm(ModelForm):
    class Meta:
        model = TipoTrabajoCantidades
        exclude = ['fecha_carga']
        labels = {
            'flg_activo': _('Tipo de trabajo activo')
        }

TipoTrabajoCantidadesFormset = inlineformset_factory(TipoTrabajo, TipoTrabajoCantidades, form=TipoTrabajoCantidadesForm,
                                                     extra=2)


class TerminacionForm(ModelForm):
    class Meta:
        model = Terminacion
        exclude = ['fecha_carga', 'terminacion_id']
        labels = {
            'flg_activo': _('Terminación activa')
        }
        widgets = {
            'tipo_terminacion': forms.Select()
        }


class ColorImpresionForm(ModelForm):
    class Meta:
        model = ColorImpresion
        exclude = ['fecha_carga', 'color_impresion_id']
        labels = {
            'flg_activo': _('Color de impresión activo')
        }


class MaquinaTerminacionForm(ModelForm):
    class Meta:
        model = MaquinaTerminacion
        exclude = ['fecha_carga', 'maquina_id', 'terminaciones']
        labels = {
            'flg_activo': _('Maquina activa')
        }


class MaquinaTerminacionTerminacionesForm(ModelForm):
    class Meta:
        model = MaquinaTerminacionTerminaciones
        exclude = ['fecha_carga', 'maquina_terminacion']
        labels = {
            'terminacion': _('Terminación'),
            'cant_max': _('Cantidad máxima'),
            'cant_max_costo_dolar': _('Costo (u$s'),
            'flg_activo': _('Combinación de Máquina y Terminación activa')
        }


MaquinaTerminacionesFormset = inlineformset_factory(MaquinaTerminacion, MaquinaTerminacionTerminaciones,\
                                                    form=MaquinaTerminacionTerminacionesForm, extra=2)


class MaquinaPliegoForm(ModelForm):
    class Meta:
        model = MaquinaPliego
        exclude = ['fecha_carga', 'maquina_id', 'colores_impresion']
        labels = {
            'flg_activo': _('Maquina activa'),
            'maquina_pliego_descripcion': _('Descripción'),
            'maquina_pliego_ult_cambio_toner': _('Último cambio de tóner/cartucho'),
            'demasia_impresion_mm': _('Demasía necesaria para los trabajos (mm)'),
        }

# Esta es necesaria, porque un color puede imprimirse con varias máquinas
class MaquinaPliegoColorImpresionForm(ModelForm):
    class Meta:
        model = MaquinaPliegoColorImpresion
        exclude = ['fecha_carga']
        labels = {
            'maquina_pliego': _('Máquina'),
            'color_impresion': _('Color'),
            'costo_dolar': _('Costo impresión (u$s)')
        }

MaquinaPliegoColorFormset = inlineformset_factory(MaquinaPliego, MaquinaPliegoColorImpresion, form=MaquinaPliegoColorImpresionForm,
                                                  extra=2)

# Esta es necesaria porque cuando llega una SP, de acuerdo al tipo de trabajo y al color requerido, el usuario va a
# poder elegir con qué máquina realizará el trabajo
class ImpresionForm(ModelForm):
    class Meta:
        model = Impresion
        exclude = ['fecha_carga']
        labels = {
            'tipo_trabajo': _('Tipo de trabajo'),
            'color_impresion': _('Color'),
            'maquina_pliego': _('Máquina'),
            'flg_activo': _('Combinacion activa'),
        }


class ServicioTecnicoForm(ModelForm):
    class Meta:
        model = ServicioTecnico
        exclude = ['fecha_carga', 'servicio_tecnico_id']
        labels = {
            'servicio_tecnico': _('Razón social'),
            'flg_activo': _('Servicio activo'),
        }

class TipoPagoForm(ModelForm):
    class Meta:
        model = TipoPago
        exclude = ['tipo_pago_id',  'fecha_carga']
        labels = {
            'tipo_pago': _('Tipo de pago'),
            'tipo_pago_recargo_porcentaje': _('Recargo (%)'),
            'flg_activo': _('Tipo de pago activo')
        }


class ComprobanteCobroForm(ModelForm):
    class Meta:
        model = ComprobanteCobro
        exclude = ['comprobante_id', 'fecha_carga']
        labels = {
            'comprobante_fecha_cobro': _('Fecha de cobro'),
            'comprobante_monto_cobro': _('Monto recibido'),
            'tipo_pago': _('Tipo de pago')
        }


class ModoEnvioForm(ModelForm):
    class Meta:
        model = ModoEnvio
        exclude = ['modo_envio_id', 'fecha_carga']
        labels = {
            'modo_envio_costo_adicional': _('Costo adicional'),
            'modo_envio_hs_aprox' : _('¿Cuánto tarda aprox? (hs)'),
            'flg_activo': _('Modo de envío activo')
        }


class SolicitudPresupuestoForm(ModelForm):
    class Meta:
        model = SolicitudPresupuesto
        exclude = ['solicitud_id', 'solicitud_fecha', 'solicitud_fecha_confirmacion', 'solicitud_email_enviado_flg',
                   'cliente']
        labels = {
            'solicitud_disenio_flg': _('Requiere diseño previo'),
            'solicitud_trabajo_alto_mm': _('Alto (mm)'),
            'solicitud_trabajo_ancho_mm': _('Ancho (mm)'),
            'solicitud_terminacion_flg': _('Requiere de terminaciones'),
            'solicitud_express_flg': _('Solicitud EXPRESS'),
            'solicitud_doble_cara_impresion_flg': _('Impresión en ambas caras'),
            'solicitud_adjuntos': _('Adjuntos'),
            'solicitud_orientacion': _('Orientación'),
            'tipo_trabajo': _('Trabajo requerido'),
            'color_impresion': _('Color de impresión'),
            'material': _('Material'),
            'envio': _('Envío')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].queryset = Material.objects.none()
        self.fields['color_impresion'].queryset = ColorImpresion.objects.none()
        self.fields['envio'].queryset = ModoEnvio.objects.none()
        self.fields['medida_estandar'].queryset = MedidaEstandar.objects.none()

class SolicitudPresupuestoTerminacionesForm(ModelForm):
    class Meta:
        model = SolicitudPresupuestoTerminaciones
        exclude = ['solicitud']
        labels = {
            'doble_cara_flg': _('Terminación para ambas caras')
        }


class PresupuestoForm(ModelForm):
    class Meta:
        model = Presupuesto
        exclude = ['solicitud', 'fecha_carga']
        labels = {
            'presupuesto_ganancia': _('Ganancia (%)'),
            'presupuesto_hojas_utilizadas': _('Hojas a utilizar (aprox)'),
            'presupuesto_precio_dolar': _('Cotización dolar'),
            'presupuesto_costo_materiales': _('Costo de materiales'),
            'presupuesto_costo_disenio': _('Costo de diseño'),
            'presupuesto_costo_unitario': _('Costo unitario'),
            'presupuesto_precio_cliente': _('Precio sugerido al cliente'),
            'maquina_pliego': _('Máquina de impresión a utilizar'),
        }
        widgets = {
            'presupuesto_hojas_utilizadas': forms.NumberInput(attrs={'disabled': True}),
            'presupuesto_costo_materiales': forms.NumberInput(attrs={'disabled': True}),
            'presupuesto_costo_unitario': forms.NumberInput(attrs={'disabled': True}),
        }


class PresupuestoTerminacionesForm(ModelForm):
    class Meta:
        model = PresupuestoTerminaciones
        exclude = ['presupuesto']
        labels = {
            'maquina_terminacion': _('Máquina de terminación'),
            'terminación': _('Terminación'),
            'costo_dolar': _('Costo terminación (u$s)')
        }
        widgets = {
            'terminacion': forms.Select(attrs={'disabled': True})
        }


class EstadoForm(ModelForm):
    class Meta:
        model = Estado
        exclude = ['estado_id', 'fecha_carga']
        labels = {
            'flg_activo': _('Estado activo'),
        }


class OrdenTrabajoForm(ModelForm):
    class Meta:
        model = OrdenTrabajo
        exclude = ['orden_id', 'solicitud', 'orden_fecha_creacion', 'estados']
        labels = {
            'orden_precio_final': _('Precio final'),
            'orden_impresion_realizada_flg': _('Impresión realizada'),
            'orden_terminacion_realizada_flg': _('Terminaciones realizadas'),
            'orden_disenio_realizado_flg': _('Diseño realizado'),
            'orden_comentarios': _('Comentarios')
        }


class OrdenTrabajoEstadoForm(ModelForm):
    class Meta:
        model = OrdenTrabajoEstado
        exclude = ['orden_trabajo']
        labels = {
            'fecha_cambio_estado': _('Fecha'),
            'personal': _('Usuario')
        }


TODO ¿Formulario para Personal?
'''