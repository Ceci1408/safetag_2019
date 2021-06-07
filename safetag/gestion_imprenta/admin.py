from django.contrib import admin
from .models import Cliente, Domicilio, Contacto, \
    Proveedor, Material, Trabajo, MedidaEstandar, Cantidad, TrabajoCantidades, Terminacion, ColorImpresion, \
    MaquinaTerminacion, TerminacionesMaquinas, \
    MaquinaPliego, MaquinaPliegoColores, ServicioTecnico, PagoRecibido, Envio, \
    SolicitudPresupuesto, SolicitudPresupuestoTerminaciones, Presupuesto, Estado, \
    OrdenTrabajo, OrdenTrabajoEstado, Personal

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Domicilio)
admin.site.register(Contacto)
admin.site.register(Proveedor)
admin.site.register(Material)
admin.site.register(Trabajo)
admin.site.register(MedidaEstandar)
admin.site.register(Cantidad)
admin.site.register(TrabajoCantidades)
admin.site.register(Terminacion)
admin.site.register(ColorImpresion)
admin.site.register(MaquinaTerminacion)
admin.site.register(TerminacionesMaquinas)
admin.site.register(MaquinaPliego)
admin.site.register(MaquinaPliegoColores)
admin.site.register(ServicioTecnico)
admin.site.register(PagoRecibido)
admin.site.register(Envio)
admin.site.register(SolicitudPresupuesto)
admin.site.register(SolicitudPresupuestoTerminaciones)
admin.site.register(Presupuesto)
admin.site.register(Estado)
admin.site.register(OrdenTrabajo)
admin.site.register(OrdenTrabajoEstado)
admin.site.register(Personal)