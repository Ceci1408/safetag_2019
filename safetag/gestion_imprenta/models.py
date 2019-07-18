from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory
from django.utils.translation import gettext_lazy as _
import re


class TipoCliente(models.Model):
    tipo_cliente_id = models.AutoField(primary_key=True)
    tipo_cliente = models.CharField(max_length=50, blank=False, null=False, unique=True,
                                    error_messages={'unique': _('Este tipo de cliente ya existe')})
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        ordering = ['tipo_cliente_id']

    def clean(self):
        if not self.tipo_cliente.isalpha():
            raise ValidationError({'tipo_cliente':_('Sólo se permiten letras')})

    def __str__(self):
        return self.tipo_cliente


class Cliente(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    cliente_ml_email = models.CharField(max_length=100, blank=True, null=True)
    cliente_original_lista_dist = models.CharField(max_length=255, blank=True, null=True)
    cliente_fecha_alta = models.DateTimeField(auto_now_add=True)
    cliente_fecha_activo = models.DateField(blank=True, null=True)
    cliente_flg_autenticado = models.BooleanField(blank=False, null=False, default=False)  # si es quien dice ser
    tipo_cliente = models.ForeignKey(TipoCliente, on_delete=models.PROTECT)

    class Meta:
        abstract = True
        ordering = ['cliente_id']


    def dar_identificacion(self):
        pass

    def dar_nombre_razon_social(self):
        pass

class ClientePf(Cliente):
    TIPO_DOC = (
        ('DNI', 'DNI'),
        ('CUIL', 'CUIL'),
        ('LC', 'LC'),
        ('LE', 'LE'),
        ('PASA', 'PASAPORTE')
    )
    cliente_nombre = models.CharField(max_length=100, blank=False, null=False)
    cliente_apellido = models.CharField(max_length=100, blank=False, null=False)
    cliente_tipo_documento = models.CharField(choices=TIPO_DOC, max_length=10, null=False, blank=False)
    cliente_nro_documento = models.CharField(max_length=12, blank=False, null=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['cliente_tipo_documento', 'cliente_nro_documento'],
                                               name='unique_tipo_nro_doc'), ]

    def clean(self):
        if not self.cliente_nombre.isalpha():
            raise ValidationError({'cliente_nombre': _('Sólo se permiten letras')})

        if not self.cliente_apellido.isalpha():
            raise ValidationError({'cliente_apellido': _('Sólo se permiten letras')})

        if not self.cliente_nro_documento.isdigit():
            raise ValidationError({'cliente_nro_documento': _('Sólo se permiten números')})

        if (self.cliente_tipo_documento in ('CUIL') and len(self.cliente_nro_documento) != 11) or \
                (self.cliente_tipo_documento not in ('CUIL') and
                 (len(self.cliente_nro_documento)<=5  or len(self.cliente_nro_documento) >= 9)):
            raise ValidationError({'cliente_nro_documento': _('La longitud del número de documento no se corresponde con el tipo de documento')})

    def dar_identificacion(self):
        return self.cliente_tipo_documento+" - "+self.cliente_nro_documento

    def dar_nombre_razon_social(self):
        return self.cliente_nombre +" "+ self.cliente_apellido


class ClientePj(Cliente):
    cliente_razon_social = models.CharField(max_length=100, blank=True, null=True)
    cliente_cuit = models.CharField(max_length=12, blank=False, null=False, unique=True,
                                    error_messages={'unique': _('Este CUIT ya existe')})

    def clean(self):
        if not self.cliente_cuit.isdigit():
            raise ValidationError({'cliente_cuit': _('Sólo se permiten números')})

    def dar_identificacion(self):
        return "CUIT -"+self.cliente_cuit

    def dar_nombre_razon_social(self):
        return self.cliente_razon_social

# TODO hacer obligatorios localidad, provincia y pais. Para hacer geolocalización


class Domicilio(models.Model):
    domicilio_id = models.AutoField(primary_key=True)
    domicilio_calle = models.CharField(max_length=100, blank=False)
    domicilio_entre_calle_1 = models.CharField(max_length=100, blank=True)
    domicilio_entre_calle_2 = models.CharField(max_length=100, blank=True)
    domicilio_entre_calle_3 = models.CharField(max_length=100, blank=True)
    domicilio_altura = models.PositiveIntegerField()
    domicilio_latitud = models.DecimalField(max_digits=12, decimal_places=10, blank=True, null=True)
    domicilio_longitud = models.DecimalField(max_digits=12, decimal_places=10, blank=True, null=True)
    pais = models.ForeignKey('Pais', models.PROTECT, blank=True, null=True)
    provincia = models.ForeignKey('Provincia', models.PROTECT, blank=True, null=True)
    localidad = models.ForeignKey('Localidad', models.PROTECT, blank=True, null=True)
    cliente_pf = models.ForeignKey(ClientePf, models.PROTECT, blank=True, null=True)
    cliente_pj = models.ForeignKey(ClientePj, models.PROTECT, blank=True, null=True)
    proveedor = models.ForeignKey('Proveedor', models.PROTECT, blank=True, null=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        ordering = ['domicilio_id']
        constraints = [models.UniqueConstraint(fields=['cliente_pf', 'domicilio_calle', 'domicilio_altura'], name='unique_domicilio_cliente_pf'),]
        constraints = [models.UniqueConstraint(fields=['cliente_pj', 'domicilio_calle', 'domicilio_altura'],
                                               name='unique_domicilio_cliente_pj'), ]


class Pais(models.Model):
    pais_id = models.AutoField(primary_key=True)
    pais = models.CharField(max_length=100, blank=False, unique=True,
                            error_messages={'unique': _('Este país ya fue ingresado')})
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    def clean(self):
        if any(p.isdigit() for p in self.pais):
            raise ValidationError({'pais': _('Sólo se permiten letras')})

    def __str__(self):
        return self.pais


class Provincia(models.Model):
    provincia_id = models.AutoField(primary_key=True)
    provincia = models.CharField(max_length=100, blank=False, unique=True,
                                 error_messages={'unique': _('Esta provincia ya fue ingresada')})
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    def clean(self):
        if any(p.isdigit() for p in self.provincia):
            raise ValidationError({'provincia': _('Sólo se permiten letras')})

    def __str__(self):
        return self.provincia


class Localidad(models.Model):
    localidad_id = models.AutoField(primary_key=True)
    localidad = models.CharField(max_length=100, blank=False)
    localidad_cp = models.PositiveIntegerField()
    pronvincia = models.ForeignKey(Provincia, on_delete=models.PROTECT)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['localidad', 'localidad_cp'], name='unique_cp_localidad'),
        ]

    def clean(self):
        if any(p.isdigit() for p in self.localidad):
            raise ValidationError({'localidad': _('Sólo se permiten letras')})

    def __str__(self):
        return self.localidad

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and (unique_check == ('localidad', 'localidad_cp')):
            return 'La localidad con el CP, ya existen'
        else:
            return super(MedidaEstandar, self).unique_error_message(model_class, unique_check)


class DatoContacto(models.Model):
    USO = (
        ('PERS', 'Personal'),
        ('LAB', 'Laboral')
    )
    TIPO_DC = (
        ('CEL', 'Celular'),
        ('TEL', 'Teléfono'),
        ('EMAIL', 'Email')
    )

    dato_contacto_id = models.AutoField(primary_key=True)
    dato_contacto_valor = models.CharField(max_length=50)
    tipo_dato_contacto = models.CharField(choices=TIPO_DC, max_length=50, blank=False, null=False)
    cliente_pf = models.ForeignKey(ClientePf, on_delete=models.CASCADE, blank=True, null=True)
    cliente_pj = models.ForeignKey(ClientePj, on_delete=models.CASCADE, blank=True, null=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE, blank=True, null=True)
    servicio_tecnico = models.ForeignKey('ServicioTecnico', on_delete=models.CASCADE, blank=True, null=True)
    dato_contacto_interno = models.PositiveSmallIntegerField(blank=True, null=True)
    dato_contacto_uso = models.CharField(choices=USO, max_length=50,blank=True, null=True)
    dato_contacto_horario_contacto = models.CharField(max_length=100, blank=True, null=False)
    dato_contacto_flg_no_llame = models.NullBooleanField()
    dato_contacto_comentarios = models.TextField()
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['dato_contacto_valor', 'tipo_dato_contacto', 'cliente_pf'],
                                    name='unique_dc_cliente_pf'),
            models.UniqueConstraint(fields=['dato_contacto_valor', 'tipo_dato_contacto', 'cliente_pj'],
                                    name='unique_dc_cliente_pj'),
        ]

    def clean(self):
        pattern = '[^@]+@[^@]+\.[^@]+'

        if self.dato_contacto_valor is not None:
            result = re.match(pattern, self.dato_contacto_valor)

            if self.tipo_dato_contacto == 'Email' and not result:
                raise ValidationError({'dato_contacto_valor': _('El dato de contacto no tiene el formato necesario')})

            if self.tipo_dato_contacto in ('Celular', 'Teléfono') and self.dato_contacto_valor.isalpha():
                raise ValidationError({'dato_contacto_valor': _('El dato de contacto no tiene el formato necesario')})

            if self.tipo_dato_contacto in ('Celular', 'Teléfono') and len(self.dato_contacto_valor) != 10:
                raise ValidationError({'dato_contacto_valor': _('El dato de contacto no tiene los dígitos correctos. Ingrese sin el cero. ')})


class Proveedor(models.Model):
    TIPO_DOC = (
        ('DNI', 'DNI'),
        ('CUIL', 'CUIL'),
        ('LC', 'LC'),
        ('LE', 'LE'),
        ('CUIT', 'CUIT'),
        ('PASA', 'PASAPORTE')
    )
    proveedor_id = models.AutoField(primary_key=True)
    proveedor_razon_social = models.CharField(max_length=100)
    proveedor_tipo_doc = models.CharField(choices=TIPO_DOC, max_length=10, blank=True, null=True)
    proveedor_nro_doc = models.CharField(max_length=12, blank=True, null=True)
    proveedor_descripcion = models.CharField(max_length=200, blank=True, null=True)
    nota_1 = models.TextField(blank=True, null=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['proveedor_tipo_doc', 'proveedor_nro_doc'], name='unique_tipo_nro_doc_proveedor'),
        ]

    def clean(self):
        if self.proveedor_nro_doc is not None:
            if not any(p.isdigit() for p in self.proveedor_nro_doc):
                raise ValidationError({'proveedor_nro_doc': _('Sólo se permiten números')})

        if self.proveedor_tipo_doc in ('CUIT', 'CUIL') and len(self.proveedor_nro_doc) != 11:
            raise ValidationError({'proveedor_nro_doc': _('La longitud del número de documento no se corresponde con el tipo de documento')})

        if self.proveedor_tipo_doc in ('DNI', 'LE', 'LC') and (5 <= len(self.proveedor_nro_doc) <= 9):
            raise ValidationError({'proveedor_nro_doc': _('La longitud del número de documento no se corresponde con el tipo de documento')})


class Material(models.Model):
    material_id = models.AutoField(primary_key=True)
    material = models.CharField(max_length=100, blank=False, null=False)
    material_alto_mm = models.IntegerField(blank=False, null=False )
    material_ancho_mm = models.IntegerField(blank=False, null=False)
    material_costo_dolar = models.DecimalField(max_digits=10, decimal_places=3, blank=False, null=False)
    material_gramaje_grs = models.IntegerField(blank=True, null=True)
    material_demasia_hoja_mm = models.DecimalField(max_digits=10, decimal_places=2,  blank=False, null=False)
    proveedores = models.ManyToManyField(Proveedor, related_name='material', blank=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    def clean(self):
        if any(p.isdigit() for p in self.material):
            raise ValidationError({'material': _('Sólo se permiten letras')})

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['material', 'material_alto_mm', 'material_ancho_mm', 'material_gramaje_grs',
                                            'material_costo_dolar'], name='unique_material'),
        ]

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('material', 'material_alto_mm', 'material_ancho_mm',
                                                          'material_gramaje_grs', 'material_costo_dolar'):
            return 'Este material ya se registró'
        else:
            return super(Material, self).unique_error_message(model_class, unique_check)


class TipoTrabajo(models.Model):
    tipo_trabajo_id = models.AutoField(primary_key=True)
    tipo_trabajo = models.CharField(max_length=50, unique=True, error_messages={'unique': _('Este tipo de trabajo ya existe')})
    tipo_trabajo_autoadhesivo_flg = models.BooleanField(blank=False, null=False)
    tipo_trabajo_doble_cara_flg = models.BooleanField(blank=False, null=False)
    tipo_trabajo_tiempo_aprox_hs = models.IntegerField(blank=True, null=True)
    tipo_trabajo_demasia_trabajo_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tipo_trabajo_circular_flg = models.BooleanField(blank=False, null=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)
    medidas = models.ManyToManyField('MedidaEstandar')
    cantidades = models.ManyToManyField('Cantidad', through='TipoTrabajoCantidades')
    terminaciones = models.ManyToManyField('Terminacion'),
    materiales = models.ManyToManyField(Material)

    def clean(self):
        if not self.tipo_trabajo.isalpha():
            raise ValidationError({'tipo_trabajo': _('Sólo se permiten letras')})


class MedidaEstandar(models.Model):
    medida_estandar_id = models.AutoField(primary_key=True)
    medida_1_cm = models.DecimalField(max_digits=10, decimal_places=2)
    medida_2_cm = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
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
        ordering = ['cantidad']


class TipoTrabajoCantidades(models.Model):
    tipo_trabajo = models.ForeignKey(TipoTrabajo, on_delete=models.PROTECT)
    cantidad = models.ForeignKey(Cantidad, on_delete=models.PROTECT)
    descuento = models.PositiveSmallIntegerField(blank=True, null=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tipo_trabajo', 'cantidad', 'descuento', 'fecha_carga', 'flg_activo'],
                                    name='unique_tipo_trabajo_cantidad'),
        ]


class TipoTerminacion(models.Model):
    tipo_terminacion_id = models.AutoField(primary_key=True)
    tipo_terminacion = models.CharField(max_length=50, null=False, unique=True,
                                        error_messages={'unique': _('Este tipo de terminación ya existe')})
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    def clean(self):
        if not self.tipo_terminacion.isalpha():
            raise ValidationError({'tipo_terminacion': _('Sólo se permiten letras')})


class Terminacion(models.Model):
    terminacion_id = models.AutoField(primary_key=True)
    terminacion = models.CharField(max_length=100, blank=False, null=False, unique=True,
                                   error_messages={'unique': _('Esta terminación ya existe')})
    terminacion_tiempo_seg = models.PositiveSmallIntegerField(blank=False, null=False)
    tipo_terminacion = models.ForeignKey(TipoTerminacion, on_delete=models.PROTECT)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    def clean(self):
        if not self.terminacion.isalpha():
            raise ValidationError({'terminacion': _('Sólo se permiten letras')})


class ColorImpresion(models.Model):
    color_impresion_id = models.AutoField(primary_key=True)
    color_impresion = models.CharField(max_length=50, null=False, blank=False, unique=True, \
                                       error_messages={'unique': _('Este color de impresión ya existe')})
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    def clean(self):
        if not self.color_impresion.isalpha():
            raise ValidationError({'color_impresion': _('Sólo se permiten letras')})


class Maquina(models.Model):
    maquina_id = models.AutoField(primary_key=True)
    maquina_marca = models.CharField(max_length=50, blank=False, null=False)
    maquina_descripcion = models.CharField(max_length=100, blank=False, null=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        abstract = True
        ordering = ['maquina_id']


class MaquinaTerminacion(Maquina):
    maquina_terminacion_descripcion = models.CharField(max_length=50, blank=True, null=True, unique=True,
                                                       error_messages={'unique': _('Esta maquina terminación ya existe')})
    terminaciones = models.ManyToManyField(Terminacion, through='MaquinaTerminacionTerminaciones')


class MaquinaTerminacionTerminaciones(models.Model):
    maquina_terminacion = models.ForeignKey(MaquinaTerminacion, on_delete=models.PROTECT)
    terminacion = models.ForeignKey(Terminacion, on_delete=models.PROTECT)
    cant_max = models.PositiveSmallIntegerField(blank=True, null=False, default=0)
    cant_max_costo_dolar = models.DecimalField(max_digits=5, decimal_places=3, blank=False, null=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['maquina_terminacion', 'terminacion', 'cant_max','fecha_carga', 'flg_activo'],
                                    name='unique_maq_terminacion_terminaciones'),
        ]


class MaquinaPliego(Maquina):
    maquina_pliego_descripcion = models.CharField(max_length=50, blank=True, null=True)
    maquina_pliego_ult_cambio_toner = models.DateField(auto_now=True)
    demasia_impresion_mm = models.PositiveSmallIntegerField(blank=False, null=False)
    colores_impresion = models.ManyToManyField(ColorImpresion, through='MaquinaPliegoColorImpresion')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['maquina_pliego_descripcion', 'fecha_carga', 'flg_activo'],
                                    name='unique_maq_pliego'),
        ]


class MaquinaPliegoColorImpresion(models.Model):
    maquina_pliego = models.ForeignKey(MaquinaPliego, on_delete=models.PROTECT)
    color_impresion = models.ForeignKey(ColorImpresion, on_delete=models.PROTECT)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)
    costo_dolar = models.DecimalField(max_digits=5, decimal_places=3, blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['maquina_pliego', 'color_impresion', 'fecha_carga', 'flg_activo'],
                                    name='unique_pliego_color'),
        ]


class Impresion(models.Model):
    tipo_trabajo = models.ForeignKey(TipoTrabajo, on_delete=models.PROTECT)
    color_impresion = models.ForeignKey(ColorImpresion, on_delete=models.PROTECT)
    maquina_pliego = models.ForeignKey(MaquinaPliego, on_delete=models.PROTECT)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tipo_trabajo', 'color_impresion','maquina_pliego','fecha_carga', 'flg_activo'],
                                    name='unique_impresion'),
        ]


class ServicioTecnico(models.Model):
    servicio_tecnico_id = models.AutoField(primary_key=True)
    servicio_tecnico = models.CharField(max_length=100, blank=False, null=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['servicio_tecnico', 'fecha_carga', 'flg_activo'],
                                    name='unique_service'),
        ]

    def clean(self):
        if not self.servicio_tecnico.isalpha():
            raise ValidationError({'servicio_tecnico': _('Sólo se permiten letras')})


class TipoPago(models.Model):
    tipo_pago_id = models.AutoField(primary_key=True)
    tipo_pago = models.CharField(max_length=50, blank=False, null=False, unique=True, \
                                 error_messages={'unique': _('Este tipo de pago ya existe')})
    tipo_pago_recargo_porcentaje = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=False, default=0)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    def clean(self):
        if not self.tipo_pago.isalpha():
            raise ValidationError({'tipo_pago': _('Sólo se permiten letras')})


class ComprobanteCobro(models.Model):
    comprobante_id = models.AutoField(primary_key=True)
    comprobante_fecha_cobro = models.DateTimeField(auto_now_add=True)
    comprobante_monto_cobro = models.DecimalField(max_digits=6, decimal_places=2, blank=False, null=False)
    tipo_pago = models.ForeignKey(TipoPago, on_delete=models.PROTECT)


class ModoEnvio(models.Model):
    modo_envio_id = models.AutoField(primary_key=True)
    modo_envio = models.CharField(max_length=50, blank=False, null=False, unique=True,\
                                  error_messages={'unique': _('Este modo de envío ya existe')})
    modo_envio_costo_adicional = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False, default=0)
    modo_envio_hs_aprox = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False, default=0)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    def clean(self):
        if not self.modo_envio.isalpha():
            raise ValidationError({'modo_envio': _('Sólo se permiten letras')})


class SolicitudPresupuesto(models.Model):
    ORIENTACION = (
        ('V', 'Vertical'),
        ('H', 'Horizontal')
    )
    solicitud_id = models.AutoField(primary_key=True)
    solicitud_fecha = models.DateTimeField(auto_now_add=True)
    solicitud_disenio_flg = models.BooleanField()
    solicitud_trabajo_alto_mm = models.IntegerField(blank=False, null=False)
    solicitud_trabajo_ancho_mm = models.IntegerField(blank=False, null=False)
    solicitud_terminacion_flg = models.BooleanField()
    solicitud_fecha_confirmacion = models.DateTimeField(blank=True, null=True)
    solicitud_express_flg = models.BooleanField()
    solicitud_doble_cara_impresion_flg = models.BooleanField()
    solicitud_adjuntos = models.FilePathField()
    solicitud_orientacion = models.CharField(choices=ORIENTACION, max_length=5, blank=True, null=True)
    solicitud_email_enviado_flg = models.BooleanField()
    cliente_pf = models.ForeignKey(ClientePf, on_delete=models.PROTECT, null=False)
    cliente_pj = models.ForeignKey(ClientePj, on_delete=models.PROTECT, null=False)
    tipo_trabajo = models.ForeignKey(TipoTrabajo, on_delete=models.PROTECT, null=False)
    color_impresion = models.ForeignKey(ColorImpresion, on_delete=models.PROTECT, null=False)
    material = models.ForeignKey(Material, on_delete=models.PROTECT, null=False)
    envio = models.ForeignKey(ModoEnvio, on_delete=models.PROTECT, null=False)


class SolicitudPresupuestoTerminaciones(models.Model):
    solicitud = models.ForeignKey(SolicitudPresupuesto, on_delete=models.PROTECT)
    terminacion = models.ForeignKey(Terminacion, on_delete=models.PROTECT)
    doble_cara_flg = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['solicitud', 'terminacion', 'doble_cara_flg'],
                                    name='unique_solcitud_terminaciones'),
        ]


class Presupuesto(models.Model):
    solicitud = models.ForeignKey(SolicitudPresupuesto, on_delete=models.PROTECT)
    presupuesto_ganancia = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    presupuesto_hojas_utilizadas = models.IntegerField(blank=False, null=False)
    presupuesto_precio_dolar = models.DecimalField(max_digits=5, decimal_places=3, blank=False, null=False)
    presupuesto_costo_materiales = models.DecimalField(max_digits=6, decimal_places=3, blank=False, null=False)
    presupuesto_costo_disenio = models.DecimalField(max_digits=6, decimal_places=3, blank=False, null=False)
    presupuesto_costo_unitario = models.DecimalField(max_digits=6, decimal_places=3, blank=False, null=False)
    presupuesto_precio_cliente = models.DecimalField(max_digits=6, decimal_places=3, blank=False, null=False)
    maquina_pliego = models.ForeignKey(MaquinaPliego, on_delete=models.PROTECT)
    fecha_carga = fecha_carga = models.DateTimeField(auto_now_add=True)


class PresupuestoTerminaciones(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.PROTECT)
    maquina_terminacion = models.ForeignKey(MaquinaTerminacion, on_delete=models.PROTECT)
    terminacion = models.ForeignKey(Terminacion, on_delete=models.PROTECT)
    costo_dolar = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)


class Estado(models.Model):
    TIPO_ESTADO = (
        ('FINAL', 'Estado final'),
        ('NO_FINAL', 'Estado no final')
    )
    estado_id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=50, blank=False, null=False, unique=True, \
                              error_messages={'unique': _('Este estado ya está registrado')})
    tipo_estado = models.CharField(choices=TIPO_ESTADO, max_length=50, null=False, blank=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)


class OrdenTrabajo(models.Model):
    orden_id = models.AutoField(primary_key=True)
    solicitud = models.OneToOneField(SolicitudPresupuesto, on_delete=models.PROTECT)
    orden_fecha_creacion = models.DateTimeField(auto_now_add=True)
    orden_precio_final = models.DecimalField(max_digits=6, decimal_places=2, blank=False, null=False)
    orden_express_flg = models.BooleanField()
    orden_impresion_realizada_flg = models.BooleanField()
    orden_terminacion_realizada_flg = models.BooleanField()
    orden_disenio_realizado_flg = models.BooleanField()
    orden_comentarios = models.TextField()
    estados = models.ManyToManyField(Estado, through='OrdenTrabajoEstado')


class OrdenTrabajoEstado(models.Model):
    orden_trabajo = models.ForeignKey(OrdenTrabajo, on_delete=models.PROTECT)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    fecha_cambio_estado = models.DateTimeField(auto_now=True)
    personal = models.ForeignKey('Personal', on_delete=models.PROTECT)


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


class TipoClienteForm(ModelForm):
    class Meta:
        model = TipoCliente
        exclude = ['tipo_cliente_id', 'fecha_carga']
        error_message = {
                            NON_FIELD_ERRORS: {
                                'unique_together': "%(field_labels)s del modelo %(model_name)s  no %(es)son %(único)s.",
                            }
                        },


class ClientePfForm(ModelForm):
    class Meta:
        model = ClientePf
        exclude = ['cliente_id', 'cliente_ml_email', 'cliente_original_lista_dist', 'cliente_fecha_alta',
                   'cliente_fecha_activo', 'cliente_flg_autenticado', ]

        error_message = {
                            NON_FIELD_ERRORS: {
                                'unique_together': "%(field_labels)s del modelo %(model_name)s  no %(es)son %(único)s.",
                            }
                        },


class ClientePjForm(ModelForm):
    class Meta:
        model = ClientePj
        exclude = ['cliente_id', 'cliente_ml_email', 'cliente_original_lista_dist', 'cliente_fecha_alta',
                   'cliente_fecha_activo', 'cliente_flg_autenticado', ]

        error_message = {
                            NON_FIELD_ERRORS: {
                                'unique_together': "%(field_labels)s del modelo %(model_name)s  no %(es)son %(único)s.",
                            }
                        },


class DomicilioForm(ModelForm):
    class Meta:
        model = Domicilio
        exclude = ['domicilio_id', 'cliente_pf', 'cliente_pj', 'proveedor', 'fecha_carga', 'domicilio_longitud',
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


class PaisForm(ModelForm):
    class Meta:
        model = Pais
        exclude = ['pais_id', 'fecha_carga']
        labels = {
            'flg_activo': _('Activo')
        }


class ProvinciaForm(ModelForm):
    class Meta:
        model = Provincia
        exclude = ['provincia_id', 'fecha_carga']
        labels = {
            'flg_activo': _('Activo')
        }


class LocalidadForm(ModelForm):
    class Meta:
        model = Localidad
        exclude = ['localidad_id', 'fecha_carga']
        labels = {
            'flg_activo': _('Activo')
        }

# TODO Este formulario si y sólo si debe llamarse cuando exista una instancia de Cliente, proveedor o Servicio Tecnico.
class DatoContactoForm(ModelForm):
    class Meta:
        model = DatoContacto
        exclude = ['dato_contacto_id', 'cliente_pf', 'cliente_pj', 'proveedor', 'servicio_tecnico', 'fecha_carga']
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
            'flg_activo': _('Cantidad activa')
        }
