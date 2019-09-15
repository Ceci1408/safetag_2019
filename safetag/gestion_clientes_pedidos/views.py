from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import SolicitudPresupuesto, SolicitudPresupuestoForm, SolicitudPresupuestoTerminacionesForm, \
    ClientePublicoForm, TipoCliente, Cliente

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index DESDE GESTION CLIENTES.")


def alta_solicitud_presupuesto(request, cliente_id):
    cliente = Cliente.objects.get(pk=cliente_id)
    if request.method == 'POST':
        form = SolicitudPresupuestoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                solicitud = form.save(commit=False)
                solicitud.cliente = cliente
                solicitud.save()
                if solicitud.solicitud_terminacion_flg:
                    return redirect('alta_sp_term', solicitud_id=solicitud.pk)
                else:
                    return redirect('index_autogestion')
    else:
        form = SolicitudPresupuestoForm(instance=cliente)
    return render(request, 'alta_solicitud_presupuesto.html', context={'cliente': cliente, 'form': form})

# TODO: hacer un checkbox de todas las terminaciones posibles!
def alta_solicitud_terminaciones(request, solicitud_id):
    solicitud = SolicitudPresupuesto.objects.get(pk=solicitud_id)

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
        tipo_cliente_prosp = TipoCliente.objects.get(pk=3)
        form = ClientePublicoForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                cli = form.save(commit=False)
                cli.tipo_cliente = tipo_cliente_prosp
                cli.save()
                return redirect('alta_sp', cliente_id=cli.pk)
    else:
        form = ClientePublicoForm()
    return render(request, 'alta/alta_cliente.html', context={'form': form})
