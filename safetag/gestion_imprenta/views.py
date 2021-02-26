from django.shortcuts import render
from .models import Cliente, Proveedor, ServicioTecnico, MaquinaTerminacion, MaquinaPliego, Contacto
from .forms import ClienteForm, ClienteContactoInlineFormset, ClienteDomicilioInlineFormset, \
    ProveedorForm, ProveedorContactoInlineFormset, ProveedorDomicilioInlineFormset, \
    ServicioTecnicoForm, ServicioTecnicoContactoInlineFormset, ServicioTecnicoDomicilioInlineFormset


# Create your views here.


def index(request):
    return render(request, 'index.html')


'''
    ALTA DE TODAS LAS ENTIDADES
'''


def alta_cliente(request):
    if request.method == 'POST':
        form_cliente = ClienteForm(request.POST)

        if form_cliente.is_valid():
            form_cliente.save()

    else:
        form_cliente = ClienteForm()

    return render(request, 'cliente/alta_cliente.html', context={'form_cliente': form_cliente})


def cliente_alta_dato_contacto(request, id_cliente):
    cliente = Cliente.objects.get(pk=id_cliente)

    if request.method == 'POST':
        formset = ClienteContactoInlineFormset(request.POST, instance=cliente, prefix='dc')
        if formset.is_valid():
            formset.save()
    else:
        formset = ClienteContactoInlineFormset(instance=cliente, prefix='dc')
    return render(request, 'cliente/alta_dato_contacto_cliente.html', context={'cliente': cliente, 'formset': formset})


def cliente_alta_domicilio(request, id_cliente):
    cliente = Cliente.objects.get(pk=id_cliente)

    if request.method == 'POST':
        formset = ClienteDomicilioInlineFormset(request.POST, instance=cliente, prefix='dom')
        if formset.is_valid():
            formset.save()
    else:
        formset = ClienteDomicilioInlineFormset(instance=cliente, prefix='dom')
    return render(request, 'cliente/alta_domicilio_cliente.html', context={'cliente': cliente, 'formset': formset})


def alta_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)

        if form.is_valid():
            form.save()
    else:
        form = ProveedorForm()
    return render(request, 'proveedor/alta_proveedor.html', context={'form': form})


def proveedor_alta_dato_contacto(request, id_proveedor):
    proveedor = Proveedor.objects.get(pk=id_proveedor)

    if request.method == 'POST':
        formset = ProveedorContactoInlineFormset(request.POST, instance=proveedor, prefix='dc')

        if formset.is_valid():
            formset.save()
    else:
        formset = ProveedorContactoInlineFormset(instance=proveedor, prefix='dc')
    return render(request, 'proveedor/alta_dato_contacto_proveedor.html', context={'proveedor': proveedor, 'formset': formset})


def proveedor_alta_domicilio(request, id_proveedor):
    proveedor = Proveedor.objects.get(pk=id_proveedor)

    if request.method == 'POST':
        formset = ProveedorDomicilioInlineFormset(request.POST, instance=proveedor, prefix='dom')

        if formset.is_valid():
            formset.save()
    else:
        formset = ProveedorDomicilioInlineFormset(instance=proveedor, prefix='dom')
    return render(request, 'proveedor/alta_domicilio_proveedor.html', context={'proveedor': proveedor, 'formset': formset})


def alta_servicio_tecnico(request):
    if request.method == 'POST':
        form = ServicioTecnicoForm(request.POST)

        if form.is_valid():
            form.save()
    else:
        form = ServicioTecnicoForm()
    return render(request, 'servicio_tecnico/alta_servicio_tecnico.html', context={'form': form})


def service_alta_dato_contacto(request, id_service):
    service = ServicioTecnico.objects.get(pk=id_service)

    if request.method == 'POST':
        formset = ServicioTecnicoContactoInlineFormset(request.POST, instance=service, prefix='st_dc')
        if formset.is_valid():
            formset.save()
    else:
        formset = ServicioTecnicoContactoInlineFormset(instance=service, prefix='st_dc')
    return render(request, 'servicio_tecnico/alta_dato_contacto_service.html', context={'service': service, 'formset': formset})


def service_alta_domicilio(request, id_service):
    service = ServicioTecnico.objects.get(pk=id_service)

    if request.method == 'POST':
        formset = ServicioTecnicoDomicilioInlineFormset(request.POST, instance=service, prefix='st_dc')
        if formset.is_valid():
            formset.save()
    else:
        formset = ServicioTecnicoDomicilioInlineFormset(instance=service, prefix='st_dc')
    return render(request, 'servicio_tecnico/alta_domicilio_service.html', context={'service': service, 'formset': formset})
