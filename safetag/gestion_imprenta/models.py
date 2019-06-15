from django.db import models
from django.contrib.auth.models import User


class TipoPersona(models.Model):
    tipo_persona_id = models.AutoField(primary_key=True)
    tipo_persona = models.CharField(max_length=50, blank=False, null=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        ordering = ['tipo_persona_id']
        constraints = [models.UniqueConstraint(fields=['tipo_persona'], name='unique_tipo_persona')]


class TipoCliente(models.Model):
    tipo_cliente_id = models.AutoField(primary_key=True)
    tipo_cliente = models.CharField(max_length=50, blank=False, null=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        ordering = ['tipo_cliente_id']
        constraints = [models.UniqueConstraint(fields=['tipo_cliente'], name='unique_tipo_cliente')]


class Cliente(models.Model):
    TIPO_DOC = (
        ('DNI', 'DNI'),
        ('CUIL', 'CUIL'),
        ('LC', 'LC'),
        ('LE', 'LE'),
        ('CUIT', 'CUIT'),
        ('PASA', 'PASAPORTE')
    )
    cliente_id = models.AutoField(primary_key=True)
    cliente_razon_social = models.CharField(max_length=100, blank=True, null=True)
    cliente_nombre = models.CharField(max_length=100, blank=True, null=True)
    cliente_apellido = models.CharField(max_length=100, blank=True, null=True)
    cliente_tipo_documento = models.CharField(choices=TIPO_DOC, max_length=10, null=False, blank=False)
    cliente_nro_documento = models.CharField(max_length=12, blank=False, null=False)
    cliente_ml_email = models.CharField(max_length=100, blank=True, null=True)
    cliente_original_lista_dist = models.CharField(max_length=255, blank=True, null=True)
    cliente_fecha_alta = models.DateTimeField(auto_now_add=True)
    cliente_fecha_activo = models.DateField(blank=True, null=True)
    cliente_flg_autenticado = models.BooleanField(blank=False, null=False)  # si es quien dice ser
    tipo_persona = models.ForeignKey(TipoPersona, on_delete=models.PROTECT)
    tipo_cliente = models.ForeignKey(TipoCliente, on_delete=models.PROTECT)

    class Meta:
        ordering = ['cliente_id']
        constraints = [models.UniqueConstraint(fields=['cliente_tipo_documento', 'cliente_nro_documento'], name='unique_tipo_nro_doc'),]


class Domicilio(models.Model):
    domicilio_id = models.AutoField(primary_key=True)
    domicilio_calle = models.CharField(max_length=100, blank=False)
    domicilio_entre_calle_1 = models.CharField(max_length=100, blank=True)
    domicilio_entre_calle_2 = models.CharField(max_length=100, blank=True)
    domicilio_entre_calle_3 = models.CharField(max_length=100, blank=True)
    domicilio_altura = models.PositiveIntegerField()
    domicilio_latitud = models.DecimalField(max_digits=12, decimal_places=10)
    domicilio_longitud = models.DecimalField(max_digits=12, decimal_places=10)
    cliente = models.ForeignKey(Cliente, models.PROTECT, blank=False, null=False)
    proveedor = models.ForeignKey('Proveedor', models.PROTECT, blank=False, null=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        ordering = ['domicilio_id']
        constraints = [models.UniqueConstraint(fields=['cliente', 'domicilio_calle', 'domicilio_altura'], name='unique_domicilio_cliente'),]


class Pais(models.Model):
    pais_id = models.AutoField(primary_key=True)
    pais = models.CharField(max_length=100, blank=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['pais'], name='unique_pais')]


class Provincia(models.Model):
    provincia_id = models.AutoField(primary_key=True)
    provincia = models.CharField(max_length=100, blank=False)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['provincia'], name='unique_provincia')]


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
            models.UniqueConstraint(fields=['localidad'], name='unique_localidad')
        ]


class TipoDatoContacto(models.Model):
    TIPO_DC = (
        ('CEL', 'Celular'),
        ('TEL', 'Teléfono'),
        ('EMAIL', 'Email')
    )
    tipo_dato_contacto_id = models.AutoField(primary_key=True)
    tipo_dato_contacto = models.CharField(choices=TIPO_DC, max_length=50)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tipo_dato_contacto'], name='unique_tipo_dato_contacto')
        ]


class DatoContacto(models.Model):
    USO = (
        ('PERS', 'Personal'),
        ('LAB', 'Laboral')
    )
    dato_contacto_id = models.AutoField(primary_key=True)
    dato_contacto_valor = models.CharField(max_length=50)
    tipo_dato_contacto = models.ForeignKey(TipoDatoContacto, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
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
            models.UniqueConstraint(fields=['dato_contacto_valor', 'tipo_dato_contacto', 'cliente'],
                                    name='unique_dc_cliente'),
        ]


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
    nota_1 = models.CharField(max_length=200, blank=True, null=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['proveedor_razon_social'], name='unique_proveedor'),
            models.UniqueConstraint(fields=['proveedor_tipo_doc', 'proveedor_nro_doc'], name='unique_tipo_nro_doc_proveedor'),
        ]


class Material(models.Model):
    material_id = models.AutoField(primary_key=True)
    material = models.CharField(max_length=100, blank=False, null=False)
    material_alto_mm = models.IntegerField(blank=False, null=False )
    material_ancho_mm = models.IntegerField(blank=False, null=False)
    material_costo_dolar = models.DecimalField(max_digits=10, decimal_places=3, blank=False, null=False)
    material_gramaje_grs = models.IntegerField(blank=True, null=True)
    material_demasia_hoja_mm = models.DecimalField(max_digits=10, decimal_places=2,  blank=False, null=False)
    proveedores = models.ManyToManyField(Proveedor)
    trabajos = models.ManyToManyField('TipoTrabajo', through='TipoTrabajoMaterial')
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)


class TipoTrabajo(models.Model):
    tipo_trabajo_id = models.AutoField(primary_key=True)
    tipo_trabajo = models.CharField(max_length=50)
    tipo_trabajo_autoadhesivo_flg = models.BooleanField(blank=False, null=False)
    tipo_trabajo_doble_cara_flg = models.BooleanField(blank=False, null=False)
    tipo_trabajo_tiempo_aprox_hs = models.IntegerField(blank=True, null=True)
    tipo_trabajo_demasia_trabajo_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tipo_trabajo_circular_flg = models.BooleanField(blank=False, null=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)
    medidas = models.ManyToManyField('MedidaEstandar')
    cantidades = models.ManyToManyField('Cantidad', through='TipoTrabajoCantidades')
    terminaciones = models.ManyToManyField('Terminacion')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tipo_trabajo'], name='unique_tipo_trabajo'),
        ]


class TipoTrabajoMaterial(models.Model):
    tipo_trabajo = models.ForeignKey(TipoTrabajo, models.PROTECT)
    material = models.ForeignKey(Material, models.PROTECT)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tipo_trabajo', 'material', 'fecha_carga', 'flg_activo'], name='unique_tipo_trabajo_material_activo'),
        ]


class MedidaEstandar(models.Model):
    medida_estandar_id = models.AutoField(primary_key=True)
    medida_1_cm = models.DecimalField(max_digits=10, decimal_places=2)
    medida_2_cm = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['medida_1_cm', 'medida_2_cm', 'fecha_carga', 'flg_activo'], name='unique_medida_estandar'),
        ]


class Cantidad(models.Model):
    cantidad_id = models.AutoField(primary_key=True)
    cantidad = models.IntegerField(blank=False, null=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cantidad', 'fecha_carga', 'flg_activo'], name='unique_cantidad'),
        ]


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
    tipo_terminacion = models.CharField(max_length=50, null=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tipo_terminacion', 'fecha_carga', 'flg_activo'],
                                    name='unique_tipo_terminacion'),
        ]


class Terminacion(models.Model):
    terminacion_id = models.AutoField(primary_key=True)
    terminacion = models.CharField(max_length=100, blank=False, null=False)
    terminacion_tiempo_seg = models.PositiveSmallIntegerField(blank=False, null=False)
    tipo_terminacion = models.ForeignKey(TipoTerminacion, on_delete=models.PROTECT)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['terminacion', 'tipo_terminacion', 'fecha_carga', 'flg_activo'],
                                    name='unique_terminacion'),
        ]


class ColorImpresion(models.Model):
    color_impresion_id = models.AutoField(primary_key=True)
    color_impresion = models.CharField(max_length=50, null=False, blank=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['color_impresion', 'fecha_carga', 'flg_activo'],
                                    name='unique_color'),
        ]


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
    maquina_terminacion_descripcion = models.CharField(max_length=50, blank=True, null=True)
    terminaciones = models.ManyToManyField(Terminacion, through='MaquinaTerminacionTerminaciones')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['maquina_terminacion_descripcion', 'fecha_carga', 'flg_activo'],
                                    name='unique_maq_terminacion'),
        ]


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


class TipoPago(models.Model):
    tipo_pago_id = models.AutoField(primary_key=True)
    tipo_pago = models.CharField(max_length=50, blank=False, null=False)
    tipo_pago_recargo_porcentaje = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=False, default=0)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tipo_pago', 'fecha_carga', 'flg_activo'],
                                    name='unique_tipo_pago'),
        ]


class ComprobanteCobro(models.Model):
    comprobante_id = models.AutoField(primary_key=True)
    comprobante_fecha_cobro = models.DateTimeField(auto_now_add=True)
    comprobante_monto_cobro = models.DecimalField(max_digits=6, decimal_places=2, blank=False, null=False)
    tipo_pago = models.ForeignKey(TipoPago, on_delete=models.PROTECT)


class ModoEnvio(models.Model):
    modo_envio_id = models.AutoField(primary_key=True)
    modo_envio = models.CharField(max_length=50, blank=False, null=False)
    modo_envio_costo_adicional = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False, default=0)
    modo_envio_hs_aprox = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False, default=0)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['modo_envio', 'fecha_carga', 'flg_activo'],
                                    name='unique_modo_envio'),
        ]


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
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    tipo_trabajo = models.ForeignKey(TipoTrabajo, on_delete=models.PROTECT)
    color_impresion = models.ForeignKey(ColorImpresion, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    envio = models.ForeignKey(ModoEnvio, on_delete=models.PROTECT)


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
    estado = models.CharField(max_length=50, blank=False, null=False)
    tipo_estado = models.CharField(choices=TIPO_ESTADO, max_length=50, null=False, blank=False)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    flg_activo = models.BooleanField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['estado', 'fecha_carga', 'flg_activo'],
                                    name='unique_estado'),
        ]


class OrdenTrabajo(models.Model):
    orden_id = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(SolicitudPresupuesto, on_delete=models.PROTECT)
    orden_fecha_creacion = models.DateTimeField(auto_now_add=True)
    orden_precio_final = models.DecimalField(max_digits=6, decimal_places=2, blank=False, null=False)
    orden_express_flg = models.BooleanField()
    orden_impresion_realizada_flg = models.BooleanField()
    orden_terminacion_realizada_flg = models.BooleanField()
    orden_disenio_realizado_flg = models.BooleanField()
    orden_comentarios = models.TextField()
    estados = models.ManyToManyField(Estado, through='OrdenTrabajoEstado')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['solicitud'], name='unique_ot'),
        ]


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
