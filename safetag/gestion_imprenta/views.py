from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import ClientePfForm, ClientePjForm, TipoClienteForm, PaisForm, ProvinciaForm, LocalidadForm, \
    ProveedorForm, MaterialForm, TipoTrabajoForm, MedidaEstandarForm, DatoContactoForm, CantidadForm, TipoTrabajo, \
    ClientePf, ClientePj, Proveedor, ServicioTecnico, ColorImpresionForm, DomicilioForm, TipoTrabajoCantidadesFormset,\
    TerminacionForm

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


'''
    ALTA DE TODAS LAS ENTIDADES
'''


def alta_tipo_cliente(request):
    if request.method == 'POST':
        form = TipoClienteForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                form = TipoClienteForm()
    else:
        form = TipoClienteForm()
    return render(request, 'alta_tipo_cliente.html', context={'form': form})

# TODO: Agregar con JS el botón de agregar más domicilios.
# TODO: Hacer que las pick lists Domiclio, Provincia y País se correspondan.


def alta_cliente_pf(request):
    if request.method == 'POST':
        form_pf = ClientePfForm(request.POST)

        if form_pf.is_valid():
            with transaction.atomic():
                form_pf.save()
    else:
        form_pf = ClientePfForm()
    return render(request, 'alta_cliente_pf.html', context={'form_pf': form_pf})


def alta_cliente_pj(request):
    if request.method == 'POST':
        form_pj = ClientePjForm(request.POST)

        if form_pj.is_valid():
            with transaction.atomic():
                form_pj.save()
    else:
        form_pj = ClientePjForm()
    return render(request, 'alta_cliente_pj.html', context={'form_pj': form_pj})


def alta_pais(request):
    if request.method == 'POST':
        form = PaisForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                form = PaisForm()
    else:
        form = PaisForm()
    return render(request, 'alta_pais.html', context={'form': form})


def alta_provincia(request):
    if request.method == 'POST':
        form = ProvinciaForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                form = ProvinciaForm()
    else:
        form = ProvinciaForm()
    return render(request, 'alta_provincia.html', context={'form': form})


def alta_localidad(request):
    if request.method == 'POST':
        form = LocalidadForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                form = LocalidadForm()
    else:
        form = LocalidadForm()
    return render(request, 'alta_localidad.html', context={'form': form})


def cliente_alta_dato_contacto(request, id_cliente):
    try:
        cliente = ClientePf.objects.get(pk=id_cliente)
    except ClientePf.DoesNotExist:
        cliente = ClientePj.objects.get(pk=id_cliente)

    if request.method == 'POST':
        form = DatoContactoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save(commit=False)
                if isinstance(cliente, ClientePf):
                    form.cliente_pf = cliente
                else:
                    form.cliente_pj = cliente
                form.save()
                form = DatoContactoForm(instance=cliente)
    else:
        form = DatoContactoForm(instance=cliente)
    return render(request, 'alta_dato_contacto.html', context={'cliente': cliente, 'form': form})


def proveedor_alta_dato_contacto(request, id_proveedor):
    proveedor = Proveedor.objects.get(pk=id_proveedor)

    if request.method == 'POST':
        form = DatoContactoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save(commit=False)
                form.proveedor = proveedor
                form.save()
                form = DatoContactoForm(instance=proveedor)
    else:
        form = DatoContactoForm(instance=proveedor)
    return render(request, 'alta_dato_contacto_prov.html', context={'proveedor': proveedor, 'form': form})


def service_alta_dato_contacto(request, id_service):
    service = ServicioTecnico.objects.get(pk=id_service)

    if request.method == 'POST':
        form = DatoContactoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save(commit=False)
                form.servicio_tecnico = service
                form.save()
                form = DatoContactoForm(instance=service)
    else:
        form = DatoContactoForm(instance=service)
    return render(request, 'alta_dato_contacto_service.html', context={'service': service, 'form': form})


def alta_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                form.save(commit=False)
    else:
        form = ProveedorForm()
    return render(request, 'alta_proveedor.html', context={'form': form})


def alta_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
               form.save()
    else:
        form = MaterialForm()
    return render(request, 'alta_material.html', context={'form': form,})


def alta_tipo_trabajo(request):
    if request.method == 'POST':
        form = TipoTrabajoForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                form.save()
    else:
        form = TipoTrabajoForm()
    return render(request, 'alta_tipo_trabajo.html', context={'form': form,})


# TODO acá posiblemente sea necesario pasar una instancia de qué trabajo estamos hablando
# TODO O sea: Luego del alta de un tipo de trabajo, que haya un botón que diga: Asociar material y me traiga acá

def alta_medida_estandar(request):
    if request.method == 'POST':
        form = MedidaEstandarForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                form = MedidaEstandarForm()
    else:
        form = MedidaEstandarForm()
    return render(request, 'alta_medida_estandar.html', context={'form': form})


def alta_cantidad(request):
    if request.method == 'POST':
        form = CantidadForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                form = CantidadForm()
    else:
        form = CantidadForm()
    return render(request, 'alta_cantidad.html', context={'form': form})


def alta_color_impresion(request):
    if request.method == 'POST':
        form = ColorImpresionForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                form = ColorImpresionForm()
    else:
        form = ColorImpresionForm()
    return render(request, 'alta_color_impresion.html', context={'form': form})


def cliente_alta_domicilio(request, id_cliente):
    try:
        cliente = ClientePf.objects.get(pk=id_cliente)
    except ClientePf.DoesNotExist:
        cliente = ClientePj.objects.get(pk=id_cliente)

    if request.method == 'POST':
        form = DomicilioForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save(commit=False)
                if isinstance(cliente, ClientePf):
                    form.cliente_pf = cliente
                else:
                    form.cliente_pj = cliente
                form.save()
                form = DomicilioForm(instance=cliente)
    else:
        form = DomicilioForm(instance=cliente)
    return render(request, 'alta_domicilio.html', context={'cliente': cliente, 'form': form})


def proveedor_alta_domicilio(request, id_proveedor):
    proveedor = Proveedor.objects.get(pk=id_proveedor)

    if request.method == 'POST':
        form = DomicilioForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save(commit=False)
                form.proveedor = proveedor
                form.save()
                form = DomicilioForm(instance=proveedor)
    else:
        form = DomicilioForm(instance=proveedor)
    return render(request, 'alta_domicilio_proveedor.html', context={'proveedor': proveedor, 'form': form})


def tipo_trabajo_cantidad(request, tipo_trabajo_id):
    trabajo = TipoTrabajo.objects.get(pk=tipo_trabajo_id)
    if request.method == 'POST':
        formset = TipoTrabajoCantidadesFormset(request.POST, instance=trabajo)
        if formset.is_valid():
            formset.save()

    else:
        formset = TipoTrabajoCantidadesFormset(instance=trabajo)
    return render(request, 'formset_tipo_trabajo_cantidad.html', {'formset': formset})


def alta_terminacion(request):
    if request.method == 'POST':
        form = TerminacionForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                form = TerminacionForm()
    else:
        form = TerminacionForm()
    return render(request, 'alta_terminacion.html', context={'form': form})


# TODO acá posiblemente sea necesario pasar una instancia de qué trabajo estamos hablando
# TODO O sea: Luego del alta de un tipo de trabajo, que haya un botón que diga: Asociar material y me traiga acá