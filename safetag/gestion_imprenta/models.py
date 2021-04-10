from django.core.exceptions import ValidationError
from django.core.validators import validate_email, validate_integer
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from math import pow, pi, ceil, floor


class Cliente(models.Model):
    ORIGEN = (
        ('formulario_presupuesto', 'Formulario de Presupuesto'),
        ('manual', 'Manual'),
    )
    cliente_id = models.AutoField(primary_key=True)
    cliente_nombre = models.CharField(max_length=100, blank=False, null=False)
    cliente_apellido = models.CharField(max_length=100, blank=False, null=False)
    cliente_fecha_alta = models.DateTimeField(auto_now_add=True)
    cliente_origen = models.CharField(choices=ORIGEN, blank=False, default='manual', max_length=25)

    class Meta:
        db_table = '"cliente"'
        ordering = ['cliente_id']
        indexes = [
            models.Index(fields=['cliente_nombre', 'cliente_apellido'], name='nombre_apellido_idx'),
            models.Index(fields=['cliente_nombre'], name='nombre_idx')
        ]
        permissions = [('elegir_origen', 'Elegir origen del cliente')]

    def clean(self):
        if not self.cliente_nombre.isalpha():
            raise ValidationError({'cliente_nombre': _('Sólo se permiten letras')})

        if not self.cliente_apellido.isalpha():
            raise ValidationError({'cliente_apellido': _('Sólo se permiten letras')})


class Domicilio(models.Model):
    TIPO_DOMICILIO = (
        ('fiscal', 'Domicilio Fiscal'),
        ('legal', 'Domicilio Legal'),
    )

    domicilio_id = models.AutoField(primary_key=True)
    domicilio_calle = models.CharField(max_length=100, blank=False)
    domicilio_altura = models.PositiveIntegerField(blank=True, null=True)
    domicilio_latitud = models.DecimalField(max_digits=12, decimal_places=10, blank=True, null=True)
    domicilio_longitud = models.DecimalField(max_digits=12, decimal_places=10, blank=True, null=True)
    pais = models.CharField(max_length=25, blank=False)
    provincia = models.CharField(max_length=25, blank=False)
    localidad = models.CharField(max_length=25, blank=False)
    cliente = models.ForeignKey(Cliente, models.PROTECT, blank=True, null=True)
    proveedor = models.ForeignKey('Proveedor', models.PROTECT, blank=True, null=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)
    servicio_tecnico = models.ForeignKey('ServicioTecnico', models.PROTECT, blank=True, null=True)
    tipo_domicilio = models.CharField(choices=TIPO_DOMICILIO, null=False, max_length=25, default='fiscal')

    class Meta:
        db_table = '"domicilio"'
        indexes = [
            models.Index(fields=['domicilio_calle', 'domicilio_altura'], name='calle_altura_idx')
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['cliente', 'domicilio_calle', 'domicilio_altura', 'localidad', 'provincia', 'pais'],
                name='unique_domicilio_cliente'),
            models.UniqueConstraint(
                fields=['proveedor', 'domicilio_calle', 'domicilio_altura', 'localidad', 'provincia', 'pais'],
                name='unique_domicilio_proveedor')
        ]

        permissions = [('agregar_laitud', 'Agregar Latitud'),
                       ('agregar_longitud', 'Agregar Longitud')]

    def clean(self):
        if not self.pais.isalpha():
            raise ValidationError({'pais': _('Sólo se permiten letras')})

    def unico_tipo_cuenta(self):
        if self.proveedor is not None and self.servicio_tecnico is None or self.cliente is None:
            return True
        elif self.proveedor is None and self.servicio_tecnico is None and self.cliente is not None:
            return True
        elif self.proveedor is None and self.servicio_tecnico is not None and self.cliente is None:
            return True
        else:
            return False


class Contacto(models.Model):
    TIPO_CONTACTO = (
        ('EMAIL', 'Email'),
        ('TEL_CEL', 'Tel / Cel')
    )

    contacto_id = models.AutoField(primary_key=True)
    contacto_horario = models.CharField(max_length=100, blank=True, null=True)
    contacto_comentarios = models.TextField(blank=True, null=True)
    dato_contacto_valor = models.CharField(max_length=50)
    tipo_dato_contacto = models.CharField(choices=TIPO_CONTACTO, max_length=25, default='EMAIL')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE, blank=True, null=True)
    servicio_tecnico = models.ForeignKey('ServicioTecnico', on_delete=models.CASCADE, blank=True, null=True)
    dato_contacto_flg_no_llame = models.BooleanField(null=True, blank=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False, default=True)

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
        if self.tipo_dato_contacto == 'EMAIL':
            try:
                validate_email(self.dato_contacto_valor)
                email_valido = True
            except ValidationError:
                email_valido = False

            if not email_valido:
                raise ValidationError({'dato_contacto_valor': _('El dato de contacto no tiene el formato esperado')})

        if self.tipo_dato_contacto == 'TEL_CEL':
            try:
                validate_integer(self.dato_contacto_valor)
                numero_valido = True
            except ValidationError:
                numero_valido = False

            if not numero_valido:
                raise ValidationError({'dato_contacto_valor': _('El dato de contacto no tiene el formato esperado')})

    def unico_tipo_cuenta(self):
        if self.proveedor is not None and self.servicio_tecnico is None or self.cliente is None:
            return True
        elif self.proveedor is None and self.servicio_tecnico is None and self.cliente is not None:
            return True
        elif self.proveedor is None and self.servicio_tecnico is not None and self.cliente is None:
            return True
        else:
            return False


class Proveedor(models.Model):
    """
    Como ya tenía proveedores, tuve que resetear el serial en proveedor_id desde PostgreSQL
    ALTER SEQUENCE proveedor_proveedor_id_seq RESTART WITH 80;
    """

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

    def __str__(self):
        return self.proveedor_razon_social


class Material(models.Model):
    material_id = models.AutoField(primary_key=True)
    material_descripcion = models.CharField(max_length=100, blank=False, null=False)
    material_alto_mm = models.IntegerField(blank=False, null=False)
    material_ancho_mm = models.IntegerField(blank=False, null=False)
    material_costo_dolar = models.DecimalField(max_digits=5, decimal_places=3, blank=False, null=False)
    material_gramaje_grs = models.IntegerField(blank=True, null=True)
    material_demasia_hoja_mm = models.IntegerField(blank=False, null=False)
    material_proveedor = models.ManyToManyField(Proveedor)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False, default=False)

    def clean(self):
        if any(p.isdigit() for p in self.material_descripcion):
            raise ValidationError({'material_descripcion': _('Sólo se permiten letras')})

        if self.material_costo_dolar < 0:
            raise ValidationError({'material_costo_dolar': _('No se admiten números negativos')})

    class Meta:
        db_table = '"material"'
        indexes = [
            models.Index(fields=['material_descripcion'], name='material_desc_idx')
        ]
        constraints = [
            models.UniqueConstraint(fields=['material_descripcion', 'material_alto_mm', 'material_ancho_mm',
                                            'material_gramaje_grs'], name='unique_material'),
        ]

    def __str__(self):
        return self.material_descripcion


class TipoTerminacion(models.Model):
    tipo_terminacion_id = models.AutoField(primary_key=True)
    tipo_terminacion = models.CharField(max_length=25, blank=False, null=False, unique=True,
                                        error_messages={'unique': _('Esta terminación ya existe')})
    flg_activo = models.BooleanField(blank=False, null=False, default=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '"tipo_terminacion"'
        constraints = [
            models.UniqueConstraint(fields=['tipo_terminacion', 'flg_activo'], name='unique_tipo_terminacion'),
        ]

    def clean(self):
        if any(tt.isdigit() for tt in self.tipo_terminacion):
            raise ValidationError({'tipo_terminacion': _('Sólo se permiten letras')})

    def __str__(self):
        return self.tipo_terminacion


class Terminacion(models.Model):
    terminacion_id = models.AutoField(primary_key=True)
    terminacion = models.CharField(max_length=100, blank=False, null=False, unique=True,
                                   error_messages={'unique': _('Esta terminación ya existe')})
    tipo_terminacion = models.ForeignKey(to=TipoTerminacion, on_delete=models.PROTECT)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        db_table = '"terminacion"'
        constraints = [
            models.UniqueConstraint(fields=['terminacion', 'flg_activo'], name='unique_terminacion'),
        ]
        indexes = [
            models.Index(fields=['terminacion'], name='terminacion_idx')
        ]

    def clean(self):
        if any(tt.isdigit() for tt in self.terminacion):
            raise ValidationError({'terminacion': _('Sólo se permiten letras')})

    def __str__(self):
        return self.terminacion


class Trabajo(models.Model):
    """
    ALTER SEQUENCE tipo_trabajo_trabajo_id_seq RESTART WITH 28;
    """
    trabajo_id = models.AutoField(primary_key=True)
    trabajo_descripcion = models.CharField(max_length=50, unique=True,
                                           error_messages={'unique': _('Este tipo de trabajo ya existe')})
    autoadhesivo_flg = models.BooleanField(blank=False, null=False)
    doble_cara_flg = models.BooleanField(blank=False, null=False)
    tiempo_aprox_hs = models.IntegerField(blank=True, null=True,
                                          help_text=_('Tiempo para realizar el trabajo (sin las terminaciones)'))
    demasia_trabajo_mm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                             help_text=_('Demasía sugerida para la impresión'))
    circular_flg = models.BooleanField(blank=False, null=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(null=False, blank=True, default=False)
    medidas = models.ManyToManyField('MedidaEstandar')
    cantidades = models.ManyToManyField('Cantidad', through='TrabajoCantidades')
    terminaciones = models.ManyToManyField(Terminacion, through='TrabajoTerminaciones', related_name='terminaciones')
    materiales = models.ManyToManyField(Material)
    maquinas_pliego = models.ManyToManyField('MaquinaPliego')

    class Meta:
        db_table = '"trabajo"'

    def clean(self):
        if self.autoadhesivo_flg and self.doble_cara_flg:
            raise ValidationError({'doble_cara_flg': _('El trabajo es autoadhesivo, no permite impresión doble faz')})

    def __str__(self):
        return self.trabajo_descripcion


class TrabajoTerminaciones(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.PROTECT)
    terminacion = models.ForeignKey(Terminacion, on_delete=models.PROTECT)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        db_table = '"trabajo_terminaciones"'
        constraints = [
            models.UniqueConstraint(fields=['trabajo', 'terminacion', 'flg_activo'],
                                    name='unique_trabajo_terminacion'),
        ]


class MedidaEstandar(models.Model):
    medida_estandar_id = models.AutoField(primary_key=True)
    medida_flg_circular = models.BooleanField()
    medida_1_cm = models.DecimalField(max_digits=6, decimal_places=2)
    medida_2_cm = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True, null=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        db_table = 'medida_estandar'
        constraints = [
            models.UniqueConstraint(fields=['medida_1_cm', 'medida_2_cm'],
                                    name='unique_medida_estandar'),
        ]
        ordering = ['medida_1_cm', 'medida_2_cm']

    def clean(self):
        if self.medida_flg_circular and self.medida_2_cm is not None:
            raise ValidationError({'medida_2_cm': _('Si la medida es circular, debe ingresar el radio en la medida 1')})

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
                                   error_messages={'unique': 'Esta cantidad ya existe'})
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return str(self.cantidad)

    class Meta:
        db_table = '"cantidad"'
        ordering = ['cantidad']
        constraints = [
            models.UniqueConstraint(fields=['cantidad'], name='unique_cantidad'),
        ]


class TrabajoCantidades(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.PROTECT)
    cantidad = models.ForeignKey(Cantidad, on_delete=models.PROTECT)
    descuento = models.PositiveSmallIntegerField(blank=True, null=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        db_table = '"trabajo_cantidades"'
        constraints = [
            models.UniqueConstraint(fields=['trabajo', 'cantidad', 'descuento', 'flg_activo'],
                                    name='unique_trabajo_cantidad'),
        ]


class ColorImpresion(models.Model):
    color_impresion_id = models.AutoField(primary_key=True)
    color_impresion = models.CharField(max_length=50, null=False, blank=False, unique=True,
                                       error_messages={'unique': _('Este color de impresión ya existe')})
    flg_activo = models.BooleanField(blank=False, null=False, default=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '"color_impresion"'
        constraints = [
            models.UniqueConstraint(fields=['color_impresion', 'flg_activo'], name='unique_color_impresion'),
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
    flg_activo = models.BooleanField(blank=False, null=False, default=False)

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
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        db_table = '"terminacion_maquinas"'
        constraints = [
            models.UniqueConstraint(fields=['maquina_terminacion', 'terminacion', 'flg_activo'],
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
    flg_activo = models.BooleanField(blank=False, null=False, default=False)
    costo_dolar = models.DecimalField(max_digits=5, decimal_places=2, blank=False)

    class Meta:
        db_table = '"maquina_pliego_colores"'
        constraints = [
            models.UniqueConstraint(fields=['maquina_pliego', 'color_impresion', 'flg_activo'],
                                    name='unique_pliego_color'),
        ]


class ServicioTecnico(models.Model):
    """
        Como ya tenía proveedores, tuve que resetear el serial en servicio_tecnico_id desde PostgreSQL
        ALTER SEQUENCE gestion_imprenta_serviciotecnico_servicio_tecnico_id_seq RESTART WITH 10;
    """
    servicio_tecnico_id = models.AutoField(primary_key=True)
    servicio_tecnico = models.CharField(max_length=100, blank=False, null=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        db_table = '"servicio_tecnico"'
        constraints = [
            models.UniqueConstraint(fields=['servicio_tecnico'], name='unique_service'),
        ]

    def clean(self):
        if not self.servicio_tecnico.isalpha():
            raise ValidationError({'servicio_tecnico': _('Sólo se permiten letras')})

    def __str__(self):
        return self.servicio_tecnico


class PagoRecibido(models.Model):
    TIPO_PAGO = (
        ('efectivo', 'Efectivo'),
        ('transf.bancaria', 'Transferencia Bancaria'),
        ('cheque', 'Cheque'),
        ('mercado pago', 'Mercado Pago')
    )

    pago_recibido_id = models.AutoField(primary_key=True)
    pego_recibido_tipo = models.CharField(choices=TIPO_PAGO, max_length=25, blank=True, null=True)
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
    modo_envio_id = models.AutoField(primary_key=True)
    modo_envio = models.CharField(max_length=20, blank=False, null=False, unique=True)
    modo_envio_porc_adicional = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    modo_envio_costo = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, default=0)
    flg_activo = models.BooleanField(blank=False, null=False, default=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '"envio"'
        constraints = [
            models.UniqueConstraint(fields=['modo_envio', 'flg_activo'],
                                    name='unique_modo_envio'),
        ]

    def __str__(self):
        return self.modo_envio

# TODO Chequear el tema de los adjuntos


class SolicitudPresupuesto(models.Model):
    ORIENTACION = (
        ('vertical', 'Vertical'),
        ('horizontal', 'Horizontal')
    )
    solicitud_id = models.AutoField(primary_key=True)
    solicitud_fecha = models.DateTimeField(auto_now_add=True)
    solicitud_disenio_flg = models.BooleanField()
    solicitud_comentarios_cliente = models.TextField(max_length=255, blank=True)
    solicitud_terminacion_flg = models.BooleanField()
    solicitud_terminaciones = models.ManyToManyField(Terminacion, through='SolicitudPresupuestoTerminaciones')
    solicitud_express_flg = models.BooleanField()
    solicitud_doble_cara_impresion_flg = models.BooleanField()
    solicitud_adjunto_1 = models.FileField(blank=True, null=True)
    solicitud_adjunto_2 = models.FileField(blank=True, null=True)
    solicitud_adjunto_3 = models.FileField(blank=True, null=True)
    solicitud_orientacion = models.CharField(choices=ORIENTACION, max_length=25, blank=True, null=True)
    trabajo = models.ForeignKey(Trabajo, on_delete=models.PROTECT, null=False)
    color_impresion = models.ForeignKey(ColorImpresion, on_delete=models.PROTECT, null=False)
    material = models.ForeignKey(Material, on_delete=models.PROTECT, null=False)
    envio = models.ForeignKey(Envio, on_delete=models.PROTECT, blank=True)
    medida_estandar = models.ForeignKey(MedidaEstandar, on_delete=models.PROTECT, null=False)
    cantidad_estandar = models.ForeignKey(Cantidad, on_delete=models.PROTECT, null=False)
    maquina_pliego = models.ForeignKey(MaquinaPliego, on_delete=models.PROTECT, blank=True, null=True)
    contacto = models.ForeignKey(Contacto, on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = '"solicitud_presupuesto"'

    def clean(self):
        if self.trabajo.autoadhesivo_flg and self.solicitud_doble_cara_impresion_flg:
            raise ValidationError({'solicitud_doble_cara_impresion_flg': _('El tipo de trabajo es autoadhesivo y '
                                                                           'no permite impresión doble faz')})

    def cantidad_hojas_impresion(self):
        area_material_mm = (self.material.material_alto_mm - self.material.material_demasia_hoja_mm) * \
                           (self.material.material_ancho_mm - self.material.material_demasia_hoja_mm)
        if self.trabajo.circular_flg:
            area_trabajo_mm = (pi * pow((self.medida_estandar.medida_1_cm * 10), 2))/4
        else:
            area_trabajo_mm = (self.medida_estandar.medida_1_cm * 10) * (self.medida_estandar.medida_2_cm * 10)

        trabajos_por_hoja = floor(area_material_mm/area_trabajo_mm)
        return ceil(self.cantidad_estandar.cantidad / trabajos_por_hoja)

    def calculo_presupuesto(self):
        # costo impresion si o si tiene que estar la maquina de impresion seteada
        maquina_pliego_color = MaquinaPliegoColores.objects.filter(maquina_pliego=self.maquina_pliego,
                                                                   color_impresion=self.color_impresion,
                                                                   flg_activo=True).first()

        try:
            costo_impresion = self.cantidad_hojas_impresion() * maquina_pliego_color.costo_dolar
        except AttributeError:
            costo_impresion = 0

        if self.solicitud_doble_cara_impresion_flg:
            costo_impresion = costo_impresion * 2

        costo_materiales = self.cantidad_hojas_impresion() * self.material.material_costo_dolar

        costo_terminaciones = 0

        if self.solicitud_terminacion_flg and SolicitudPresupuestoTerminaciones.objects.filter(solicitud=self).exists():
            solicitud_terminaciones = SolicitudPresupuestoTerminaciones.objects.filter(solicitud=self)

            for t in solicitud_terminaciones:
                try:
                    costo_terminacion = TerminacionesMaquinas.objects.filter(maquina_terminacion=t.maquina_terminacion,
                                                                             terminacion=t.terminacion,
                                                                             flg_activo=True).first().costo_dolar
                    if t.doble_cara_flg:
                        costo_terminaciones = costo_terminacion * 2 * self.cantidad_hojas_impresion() + \
                                              costo_terminaciones
                    else:
                        costo_terminaciones = costo_terminacion * self.cantidad_hojas_impresion() + costo_terminaciones
                except AttributeError:
                    costo_terminacion = 0

        return costo_impresion, costo_materiales, costo_terminaciones


class SolicitudPresupuestoTerminaciones(models.Model):
    solicitud = models.ForeignKey(SolicitudPresupuesto, on_delete=models.PROTECT)
    terminacion = models.ForeignKey(Terminacion, on_delete=models.PROTECT)
    doble_cara_flg = models.BooleanField(null=True, default=False)
    maquina_terminacion = models.ForeignKey(MaquinaTerminacion, on_delete=models.PROTECT, null=True)
    comentarios = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = '"solicitud_terminaciones"'


class Presupuesto(models.Model):
    solicitud = models.ForeignKey(SolicitudPresupuesto, on_delete=models.PROTECT)
    margen_ganancia = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    hojas_utilizadas = models.IntegerField(blank=False, null=False)
    costo_impresion_dolar = models.DecimalField(max_digits=5, decimal_places=3, blank=False, null=False)
    cotizacion_dolar = models.DecimalField(max_digits=6, decimal_places=3, blank=False, null=False)
    costo_disenio = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    costo_unitario_dolar = models.DecimalField(max_digits=6, decimal_places=3, blank=False, null=False)
    costo_total_dolar = models.DecimalField(max_digits=7, decimal_places=3, blank=False, null=False)
    precio_cliente = models.DecimalField(max_digits=7, decimal_places=3, blank=False, null=False)
    costo_material_dolar = models.DecimalField(max_digits=6, decimal_places=3, blank=False, null=False)
    costo_terminaciones_dolar = models.DecimalField(max_digits=6, decimal_places=3, blank=False, null=False)
    fecha_carga = fecha_carga = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)

    class Meta:
        db_table = '"presupuesto"'
        ordering = ['-fecha_carga']

    def ultimo_estado(self):
        ultimo_estado_presupuesto = self.presupuestoestado_set.all().order_by('-fecha_cambio_estado')[0]
        return ultimo_estado_presupuesto


class PresupuestoEstado(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.PROTECT)
    estado = models.ForeignKey('Estado', on_delete=models.PROTECT, limit_choices_to={'entidad_asociada': 'presupuesto'})
    fecha_cambio_estado = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = '"presupuesto_estados"'
        ordering = ['presupuesto', '-fecha_cambio_estado']


class Estado(models.Model):
    TIPO_ESTADO = (
        ('Final', 'Estado final'),
        ('Intermedio', 'Estado intermedio'),
        ('Inicial', 'Estado inicial')
    )
    ENTIDAD = (
        ('orden_trabajo', 'Orden de Trabajo'),
        ('presupuesto', 'Presupuesto')
    )
    estado_id = models.AutoField(primary_key=True)
    estado_descripcion = models.CharField(max_length=50, blank=False)
    tipo_estado = models.CharField(choices=TIPO_ESTADO, max_length=25, null=False, blank=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False, default=False)
    estado_secuencia = models.PositiveSmallIntegerField(blank=False, default=1)
    entidad_asociada = models.CharField(choices=ENTIDAD, max_length=50, blank=False, default='orden_trabajo')

    class Meta:
        db_table = '"estado"'
        constraints = [
            models.UniqueConstraint(fields=['estado_descripcion', 'tipo_estado', 'flg_activo','estado_secuencia','entidad_asociada'],
                                    name='unique_tipo_estado'),
        ]

    def __str__(self):
        return self.estado_descripcion


class Subestado(models.Model):
    subestado_id = models.AutoField(primary_key=True)
    subestado = models.CharField(max_length=50, blank=False, null=False)
    estado = models.ForeignKey(to=Estado, on_delete=models.PROTECT,)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        db_table = '"subestado"'
        constraints = [
            models.UniqueConstraint(fields=['estado', 'subestado', 'flg_activo'],
                                    name='unique_subestado'),
        ]


class OrdenTrabajo(models.Model):
    orden_id = models.AutoField(primary_key=True)
    presupuesto = models.OneToOneField(Presupuesto, on_delete=models.PROTECT, blank=True, null=True)
    orden_fecha_creacion = models.DateTimeField(auto_now_add=True)
    orden_impresion_realizada_flg = models.BooleanField(blank=True)
    orden_terminacion_realizada_flg = models.BooleanField(blank=True)
    orden_disenio_realizado_flg = models.BooleanField(blank=True)
    estados = models.ManyToManyField(Estado, through='OrdenTrabajoEstado')

    class Meta:
        db_table = '"orden_trabajo"'
        ordering = ['orden_fecha_creacion']

    def ultimo_estado(self):
        ultimo_estado_ot = self.ordentrabajoestado_set.all().order_by('-fecha_cambio_estado')[0]
        return ultimo_estado_ot


class OrdenTrabajoEstado(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_cambio_estado = models.DateTimeField(auto_now_add=True)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, limit_choices_to={'entidad_asociada':'orden_trabajo'})
    orden_trabajo = models.ForeignKey(OrdenTrabajo, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = '"orden_trabajo_estados"'
        ordering = ['orden_trabajo', 'estado']


class Comentario(models.Model):
    solicitud = models.ForeignKey(SolicitudPresupuesto, on_delete=models.PROTECT, null=True)
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.PROTECT, null=True)
    orden = models.ForeignKey(OrdenTrabajo, on_delete=models.PROTECT, null=True)
    fecha_comentario = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(max_length=100, blank=True)
    # TODO que guarde el usuario logueado
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = '"comentarios"'
        ordering = ['-fecha_comentario']
