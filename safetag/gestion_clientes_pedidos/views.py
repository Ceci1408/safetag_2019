import datetime

from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Material, Cantidad, \
    SolicitudPresupuestoForm, MedidaEstandar, Trabajo, SpTerminacionesFormset, SpContactoFormset, Cliente, \
    ColorImpresion, Envio, Terminacion, Contacto


def index(request):
    return render(request, 'index_autogestion.html')


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
            solicitud = form_sp.save()

            for form in formset_contacto:
                tipo_dato_contacto = form.cleaned_data.get('tipo_dato_contacto', None)
                dato_contacto = form.cleaned_data.get('dato_contacto_valor', None)
                prosp_nombre = form.cleaned_data.get('prosp_nombre', None)
                prosp_apellido = form.cleaned_data.get('prosp_apellido', None)

                try:
                    contacto = Contacto.objects.get(tipo_dato_contacto=tipo_dato_contacto,
                                                    dato_contacto_valor=dato_contacto, cliente__isnull=False)
                except Contacto.DoesNotExist:
                    contacto = Contacto(tipo_dato_contacto=tipo_dato_contacto, dato_contacto_valor=dato_contacto)
                    cliente_nuevo = Cliente()
                    cliente_nuevo.cliente_nombre = prosp_nombre
                    cliente_nuevo.cliente_apellido = prosp_apellido
                    cliente_nuevo.cliente_origen = 'formulario_presupuesto'
                    cliente_nuevo.save()
                    contacto.cliente = cliente_nuevo
                    contacto.save()
                finally:
                    solicitudes = contacto.solicitudes_asociadas()

                    if solicitudes:
                        tz_info = solicitudes[0].fecha_creacion.tzinfo
                        # si el mismo dato de contacto se usó en un form hace menos de una hora, no avanza
                        if (datetime.datetime.now(tz_info) - solicitudes[0].fecha_creacion).total_seconds() / 3600 < 1:
                            return redirect(to='reintento')

                    solicitud.contactos.add(contacto)

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


def reintento(request):
    return render(request, 'alta/reintento.html')