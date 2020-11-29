from django.db import transaction
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from .models import SolicitudPresupuesto, Cliente, Trabajo, Material, ColorImpresion, Envio, Terminacion, \
    MedidaEstandar, SolicitudPresupuestoForm, SolicitudPresupuestoTerminacionesForm
import json

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index DESDE GESTION CLIENTES.")


def alta_solicitud_presupuesto(request):
    if request.method == 'POST':
        form_sp = SolicitudPresupuestoForm(request.POST, prefix='sp')
        form_spt = SolicitudPresupuestoTerminacionesForm(request.POST, prefix='spt')
        if form_sp.is_valid() and form_spt.is_valid():
            return HttpResponse('Thanks')

    else:
        form_sp = SolicitudPresupuestoForm(prefix='sp')
        form_spt = SolicitudPresupuestoTerminacionesForm(prefix='spt')
    return render(request, 'alta/alta_solicitud_presupuesto.html', context={'form_sp': form_sp,
                                                                            'form_spt': form_spt})


def carga_material(request):
    trabajo_id = request.GET.get('trabajo')
    materiales = Material.objects.filter(trabajo__trabajo_id=trabajo_id).order_by('material_descripcion')
    #values('pk', 'material_descripcion')
    medidas = MedidaEstandar.objects.filter(trabajo__trabajo_id=trabajo_id).order_by('medida_estandar_id')
    #    values('pk', 'medida_1_cm', 'medida_2_cm')

    materiales_serial = serializers.serialize('json', materiales, fields=('material_descripcion'))
    medidas_serial = serializers.serialize('json', medidas, fields=('medida_1_cm', 'medida_2_cm'))

    json_response = JsonResponse({'materiales': materiales_serial,
                                  'medidas': medidas_serial}, safe=False)
    return json_response
    #return render(request, 'dropdown_lists/medidas_ddl.html', {'materiales':materiales,
    #                                                              'medidas': medidas})


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

def alta_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                #cli.save()
                #return redirect('alta_sp', cliente_id=cli.pk)
                return render(request, 'alta/medidas_ddl.html', context={''})
    else:
        form = ClienteForm()
    return render(request, 'alta/alta_cliente.html', context={'form': form})
'''