from django.contrib import admin
from .models import TipoCliente, ClientePj, ClientePf, Domicilio, Pais, Provincia, Localidad, DatoContacto, \
    Proveedor, Material, TipoTrabajo, MedidaEstandar, Cantidad, TipoTrabajoCantidades, Terminacion, ColorImpresion, MaquinaTerminacion, MaquinaTerminacionTerminaciones, \
    MaquinaPliego, MaquinaPliegoColorImpresion,  Impresion, ServicioTecnico, TipoPago, ComprobanteCobro, ModoEnvio, \
    SolicitudPresupuesto, SolicitudPresupuestoTerminaciones, Presupuesto, PresupuestoTerminaciones, Estado, \
    OrdenTrabajo, OrdenTrabajoEstado, Personal

# Register your models here.
admin.site.register(TipoCliente)
admin.site.register(ClientePf)                    
admin.site.register(ClientePj) 
admin.site.register(Domicilio)
admin.site.register(Pais)
admin.site.register(Provincia)
admin.site.register(Localidad)
admin.site.register(DatoContacto)
admin.site.register(Proveedor)
admin.site.register(Material)
admin.site.register(TipoTrabajo)
admin.site.register(MedidaEstandar)
admin.site.register(Cantidad)
admin.site.register(TipoTrabajoCantidades)
admin.site.register(Terminacion)
admin.site.register(ColorImpresion)
admin.site.register(MaquinaTerminacion)
admin.site.register(MaquinaTerminacionTerminaciones)
admin.site.register(MaquinaPliego)
admin.site.register(MaquinaPliegoColorImpresion)
admin.site.register(Impresion)
admin.site.register(ServicioTecnico)
admin.site.register(TipoPago)
admin.site.register(ComprobanteCobro)
admin.site.register(ModoEnvio)
admin.site.register(SolicitudPresupuesto)
admin.site.register(SolicitudPresupuestoTerminaciones)
admin.site.register(Presupuesto)
admin.site.register(PresupuestoTerminaciones)
admin.site.register(Estado)
admin.site.register(OrdenTrabajo)
admin.site.register(OrdenTrabajoEstado)
admin.site.register(Personal)