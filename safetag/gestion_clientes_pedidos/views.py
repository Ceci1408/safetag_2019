from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import SolicitudPresupuesto, Cliente, Trabajo, Material, ColorImpresion, Envio, Terminacion, \
    MedidaEstandar, SolicitudPresupuestoForm
import json

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index DESDE GESTION CLIENTES.")


def alta_solicitud_presupuesto(request):
    if request.method == 'POST':
        form = SolicitudPresupuestoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                '''solicitud = form.save(commit=False)
                solicitud.cliente = cliente
                solicitud.save()
                if solicitud.solicitud_terminacion_flg:
                    return redirect('alta_sp_term', solicitud_id=solicitud.pk)
                else:
                    return redirect('index_autogestion')'''
                return HttpResponse('test')
    else:
        form = SolicitudPresupuestoForm()
    return render(request, 'alta/alta_solicitud_presupuesto.html', context={'form': form})


def carga_material_ajax(request):
    tipo_trabajo_id = request.GET.get('tipo_trabajo')
    materiales = Material.objects.filter(tipotrabajo__tipo_trabajo_id=tipo_trabajo_id).order_by('material')
    # Todos los trabajos aceptan los mismos colores de impresión. Si el día de mañana, un tipo de trabajo va a estar vinculado
    # a un color particular, se agrega una relación N a N en TipoTrabajo y acá se hace como los
    # anteriores...
    colores = ColorImpresion.objects.all()
    # Todos los trabajos aceptan los mismos modos de envío. Si el día de mañana, un tipo de trabajo va a estar vinculado
    # a un modo de envío particular, se agrega una relación N a N en SolicitudPresupuesto y acá se hace como los
    # anteriores...
    modo_envio = Envio.objects.all()
    medidas = MedidaEstandar.objects.filter(tipotrabajo__tipo_trabajo_id=tipo_trabajo_id).order_by('medida_estandar_id')

    # return render(request, 'dropdown_lists/solicitud_presupuesto.html', {'materiales': materiales,
    #                                                                      'colores': colores,
    #                                                                      'modo_envio': modo_envio,
    #                                                                      'medidas': medidas})
    mat = []
    for id, m in materiales:
        mat.append((id, m))
    return HttpResponse(json.dumps({'materiales': materiales, 'colores':colores}))
'''
'''

# TODO: hacer un checkbox de todas las terminaciones posibles!
'''
def alta_solicitud_terminaciones(request, solicitud_id):
    solicitud = SolicitudPresupuesto.objects.get(pk=solicitud_id)
    tipo_trabajo_elegido = solicitud.tipo_trabajo

    if request.method == 'POST':
        form = SolicitudPresupuestoTerminacionesForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                sol_terminacion = form.save(commit=False)
                sol_terminacion.solicitud = solicitud
                sol_terminacion.save()
                return redirect('index_autogestion')
    else:
        form = SolicitudPresupuestoTerminacionesForm()
    return render(request, 'alta_solicitud_terminaciones.html', context={'solicitud': solicitud, 'form': form})

'''
def alta_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                #cli.save()
                #return redirect('alta_sp', cliente_id=cli.pk)
                return render(request, 'alta/alta_solicitud_presupuesto.html', context={''})
    else:
        form = ClienteForm()
    return render(request, 'alta/alta_cliente.html', context={'form': form})
