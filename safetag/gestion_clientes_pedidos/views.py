from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from .models import Material, Cantidad, \
    SolicitudPresupuestoForm, MedidaEstandar, Trabajo, SpTerminacionesFormset, SpContactoFormset, Cliente, \
    ColorImpresion, Envio, Terminacion


def index(request):
    return HttpResponse("Hello, world. You're at the polls index DESDE GESTION CLIENTES.")


def alta_solicitud_presupuesto(request):
    trabajos_vigentes = Trabajo.objects.filter(flg_activo=True)
    colores_vigentes = ColorImpresion.objects.filter(flg_activo=True)
    materiales_vigentes = Material.objects.filter(flg_activo=True)
    envios_vigentes = Envio.objects.filter(flg_activo=True)
    medidas_vigentes = MedidaEstandar.objects.filter(flg_activo=True)
    cantidades_vigentes = Cantidad.objects.filter(flg_activo=True)
    terminaciones_vigentes = Terminacion.objects.filter(flg_activo=True)

    if request.method == 'POST':
        form_sp = SolicitudPresupuestoForm(request.POST, request.FILES, prefix='sp')
        formset = SpTerminacionesFormset(request.POST, prefix='spt')
        formset_contacto = SpContactoFormset(request.POST, prefix='spc')

        if form_sp.is_valid() and formset.is_valid() and formset_contacto.is_valid():
            contacto = None
            for f in formset_contacto:
                contacto = f.save(commit=False)
                cliente_nuevo = Cliente()
                cliente_nuevo.cliente_nombre = f.cleaned_data.get('prosp_nombre')
                cliente_nuevo.cliente_apellido = f.cleaned_data.get('prosp_apellido')
                cliente_nuevo.cliente_origen = 'formulario_presupuesto'
                cliente_nuevo.save()
                contacto.cliente = cliente_nuevo
                contacto.save()

            solicitud = form_sp.save(commit=False)
            solicitud.contacto = contacto
            solicitud.save()

            if solicitud.solicitud_terminacion_flg:
                for f in formset:
                    solicitud_terminacion = f.save(commit=False)
                    solicitud_terminacion.solicitud = solicitud
                    solicitud_terminacion.save()

            return redirect(to='thankyou')

    else:
        form_sp = SolicitudPresupuestoForm(prefix='sp')
        form_sp.fields['trabajo'].queryset = trabajos_vigentes
        form_sp.fields['color_impresion'].queryset = colores_vigentes
        form_sp.fields['material'].queryset = materiales_vigentes
        form_sp.fields['envio'].queryset = envios_vigentes
        form_sp.fields['medida_estandar'].queryset = medidas_vigentes
        form_sp.fields['cantidad_estandar'].queryset = cantidades_vigentes

        formset = SpTerminacionesFormset(prefix='spt')

        for f in formset:
            f.fields['terminacion'].queryset = terminaciones_vigentes

        formset_contacto = SpContactoFormset(prefix='spc')

    return render(request, 'alta/alta_solicitud_presupuesto.html', context={'form_sp': form_sp,
                                                                            'formset': formset,
                                                                            'formset_contacto': formset_contacto})


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


def thankyoupage(request):
    return render(request, 'alta/thankyou_page.html')