from django import template

register = template.Library()


@register.filter(name='check_maquina_terminacion')
def check_maquina_terminacion(value):
    a = any(x.maquina_terminacion is None for x in value)
    return a


@register.filter(name='check_presupuesto_sin_aceptar')
def check_presupuesto_sin_aceptar(value):
    estado_buscar = 'Aceptado por el cliente'
    resultado = estado_buscar in (pe.estado.estado_descripcion for presupuesto in value for pe in presupuesto.presupuestoestado_set.all())
    return resultado
