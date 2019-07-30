from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse
from .models import SolicitudPresupuesto, SolicitudPresupuestoForm, SolicitudPresupuestoTerminacionesForm

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index DESDE GESTION CLIENTES.")


def alta_solicitud_presupuesto(request):
    if request.method == 'POST':
        form = SolicitudPresupuestoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                form = SolicitudPresupuestoForm()
    else:
        form = SolicitudPresupuestoForm()
    return render(request, 'alta_solicitud_presupuesto.html', context={'form': form})