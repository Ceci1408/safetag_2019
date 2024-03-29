from django.contrib import admin
from .models import *

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
admin.site.register(TipoTerminacion)
admin.site.register(TrabajoTerminaciones)
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
admin.site.register(PresupuestoEstado)
admin.site.register(Estado)
admin.site.register(Tarea)
admin.site.register(TareaHistorial)
admin.site.register(OrdenTrabajo)
admin.site.register(OrdenTrabajoEstado)
admin.site.register(Comentario)
