from django.core import serializers
from django.forms import inlineformset_factory
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from .models import Material, Cantidad, \
    SolicitudPresupuestoForm, MedidaEstandar, SolicitudPresupuesto, SolicitudPresupuestoTerminaciones, Trabajo, \
    TerminacionesFormset, Terminacion

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index DESDE GESTION CLIENTES.")


def alta_solicitud_presupuesto(request):
    if request.method == 'POST':
        form_sp = SolicitudPresupuestoForm(request.POST, request.FILES, prefix='sp')
        formset = TerminacionesFormset(request.POST)

        if form_sp.is_valid() and formset.is_valid():
            form_sp.save(commit=False)

            for sp_terminacion in formset:
                sp_terminacion.save(commit=False)
                sp_terminacion.solicitud = form_sp
                sp_terminacion.save()
            return HttpResponse('yeah')
        elif form_sp.is_valid():
            #formulario_sp = form_sp.save()
            pass
            return HttpResponse('Thanks')
    else:
        form_sp = SolicitudPresupuestoForm(prefix='sp')
        formset = TerminacionesFormset()
    return render(request, 'alta/alta_solicitud_presupuesto.html', context={'form_sp': form_sp, 'formset': formset})
'''
        if form_sp.is_valid() and form_sp.cleaned_data.get('solicitud_terminacion_flg'):
            solicitud = form_sp.save()
            return redirect('alta_sp_terminaciones', solicitud_pk=solicitud.pk)
'''

def alta_solicitud_terminaciones(request, solicitud_pk):
    SolicitudesTerminacionesFormSet = inlineformset_factory(parent_model=SolicitudPresupuesto,
                                                            model=SolicitudPresupuestoTerminaciones,
                                                            exclude=('solicitud', 'maquina_terminacion'), extra=3,
                                                            can_delete=True, max_num=5, validate_max=True)
    solicitud = SolicitudPresupuesto.objects.get(pk=solicitud_pk)
    #trabajos = Trabajo.objects.
    if request.method == "POST":
        formset_terminaciones = SolicitudesTerminacionesFormSet(request.POST, request.FILES, prefix='spt', instance=solicitud)

        if formset_terminaciones.is_valid():
            pass
    else:
        formset_terminaciones = SolicitudesTerminacionesFormSet(prefix='spt', instance=solicitud)

    return render(request, 'alta/alta_sp_terminaciones.html', context={'formset_spt': formset_terminaciones})


def carga_relaciones(request):
    trabajo_id = request.GET.get('trabajo')
    materiales = Material.objects.filter(trabajo__trabajo_id=trabajo_id).order_by('material_descripcion')
    medidas = MedidaEstandar.objects.filter(trabajo__trabajo_id=trabajo_id).order_by('medida_estandar_id')
    cantidades = Cantidad.objects.filter(trabajo__trabajo_id=trabajo_id).order_by('cantidad_id')
    terminaciones = Trabajo.objects.get(trabajo_id=trabajo_id).terminaciones.all().order_by('terminacion_id')

    materiales_serial = serializers.serialize('json', materiales, fields=('material_descripcion'))
    medidas_serial = serializers.serialize('json', medidas, fields=('medida_1_cm', 'medida_2_cm'))
    cantidades_serial = serializers.serialize('json', cantidades, fields=('cantidad'))
    terminaciones = serializers.serialize('json', terminaciones, fields=('terminacion'))


    json_response = JsonResponse({'materiales': materiales_serial,
                                  'medidas': medidas_serial,
                                  'cantidades':cantidades_serial,
                                  'terminaciones': terminaciones}, safe=False)
    return json_response

'''
def alta_solicitud_terminaciones(request):


    if request.method == 'POST':

        if formset_terminaciones.is_valid():
            print('holis')
    else:
        formset_terminaciones = SolicitudesTerminacionesFormSet(data)

    return render(request, 'alta_sp_terminaciones.html', {'formset': formset_terminaciones})
'''

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