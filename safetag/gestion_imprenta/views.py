from django.shortcuts import render, redirect
from decimal import Decimal
from .forms import *
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from datetime import datetime


def index(request):
    return render(request, 'index.html')


""" Cliente """


@login_required
def alta_cliente(request):
    if request.method == 'POST':
        form_cliente = ClienteForm(request.POST)

        if form_cliente.is_valid():
            form_cliente.save()
            return redirect(to='index')
    else:
        form_cliente = ClienteForm()
        form_cliente.fields['cliente_origen'].choices = [('manual','Manual')]
    return render(request, 'base_alta_entidad.html', context={'form': form_cliente, 'modelo': 'Cliente'})


@login_required
@permission_required('gestion_imprenta.add_contacto', 'gestion_imprenta.change_contacto', raise_exception=True)
def cliente_alta_dato_contacto(request, id_cliente):
    cliente = Cliente.objects.get(pk=id_cliente)

    if request.method == 'POST':
        formset = ClienteContactoInlineFormset(request.POST, instance=cliente, prefix='dc')
        if formset.is_valid():
            formset.save()
            return redirect(to='detalle_cliente', pk=cliente.pk)
    else:
        formset = ClienteContactoInlineFormset(instance=cliente, prefix='dc')
    return render(request, 'base_formset.html', context={'cliente': cliente,
                                                         'formset': formset,
                                                         'template_name': 'resumen/resumen_cliente.html',
                                                         'modelo': 'Cliente',
                                                         'titulo': 'Dato de Contacto',
                                                         'id': cliente.pk,
                                                         'nombre_vista': 'cliente_alta_dc'})


@login_required
@permission_required('gestion_imprenta.add_domicilio', 'gestion_imprenta.change_domicilio', raise_exception=True)
def cliente_alta_domicilio(request, id_cliente):
    cliente = Cliente.objects.get(pk=id_cliente)

    if request.method == 'POST':
        formset = ClienteDomicilioInlineFormset(request.POST, instance=cliente, prefix='dom')
        if formset.is_valid():
            formset.save()
            return redirect(to='detalle_cliente', pk=cliente.pk)
    else:
        formset = ClienteDomicilioInlineFormset(instance=cliente, prefix='dom')
    return render(request, 'base_formset.html', context={'cliente': cliente,
                                                         'formset': formset,
                                                         'template_name': 'resumen/resumen_cliente.html',
                                                         'modelo': 'Cliente',
                                                         'titulo': 'Domicilio',
                                                         'id': cliente.pk,
                                                         'nombre_vista': 'cliente_alta_domicilio'})


class ListaClientes(LoginRequiredMixin, ListView):
    queryset = Cliente.objects.all()
    template_name = "listas/cliente_lista.html"
    context_object_name = 'lista'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Clientes'
        return context


class DetalleCliente(LoginRequiredMixin, DetailView):
    template_name = 'detalle/cliente_detalle.html'
    queryset = Cliente.objects.all()
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = context.get('cliente').cliente_nombre + " " + context.get('cliente').cliente_apellido

        return context


@login_required
@permission_required('gestion_imprenta.add_proveedor', raise_exception=True)
def alta_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to='index')
    else:
        form = ProveedorForm()
    return render(request, 'base_alta_entidad.html', context={'form': form, 'modelo': 'Proveedor'})


@login_required
@permission_required('gestion_imprenta.add_contacto', raise_exception=True)
def proveedor_alta_dato_contacto(request, id_proveedor):
    proveedor = Proveedor.objects.get(pk=id_proveedor)

    if request.method == 'POST':
        formset = ProveedorContactoInlineFormset(request.POST, instance=proveedor, prefix='dc')

        if formset.is_valid():
            formset.save()
            return redirect(to='index')
        else:
            pass
    else:
        formset = ProveedorContactoInlineFormset(instance=proveedor, prefix='dc')
    return render(request, 'base_formset.html', context={'proveedor': proveedor,
                                                         'formset': formset,
                                                         'template_name': 'resumen/resumen_proveedor.html',
                                                         'modelo': 'Proveedor',
                                                         'titulo': 'Dato de Contacto',
                                                         'id': proveedor.pk,
                                                         'nombre_vista': 'proveedor_alta_dc'})


@login_required
@permission_required('gestion_imprenta.add_domicilio', raise_exception=True)
def proveedor_alta_domicilio(request, id_proveedor):
    proveedor = Proveedor.objects.get(pk=id_proveedor)

    if request.method == 'POST':
        formset = ProveedorDomicilioInlineFormset(request.POST, instance=proveedor, prefix='dom')

        if formset.is_valid():
            formset.save()
            return redirect(to='index')
    else:
        formset = ProveedorDomicilioInlineFormset(instance=proveedor, prefix='dom')
    return render(request, 'base_formset.html', context={'proveedor': proveedor,
                                                         'formset': formset,
                                                         'template_name': 'resumen/resumen_proveedor.html',
                                                         'modelo': 'Proveedor',
                                                         'titulo': 'Domicilio',
                                                         'id': proveedor.pk,
                                                         'nombre_vista': 'proveedor_alta_domicilio'})


class ListaProveedores(LoginRequiredMixin, ListView):
    queryset = Proveedor.objects.all()
    template_name = "listas/proveedor_lista.html"
    context_object_name = 'lista'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Proveedores'
        return context


class DetalleProveedor(LoginRequiredMixin, DetailView):
    template_name = 'detalle/proveedor_detalle.html'
    queryset = Proveedor.objects.all()
    context_object_name = 'proveedor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = context.get('proveedor').proveedor_razon_social

        return context


@login_required
@permission_required('gestion_imprenta.add_serviciotecnico', raise_exception=True)
def alta_servicio_tecnico(request):
    if request.method == 'POST':
        form = ServicioTecnicoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to='index')
    else:
        form = ServicioTecnicoForm()
    return render(request, 'base_alta_entidad.html', context={'form': form, 'modelo': 'Servicio Técnico'})


@login_required
@permission_required('gestion_imprenta.add_contacto', raise_exception=True)
def service_alta_dato_contacto(request, id_service):
    service = ServicioTecnico.objects.get(pk=id_service)

    if request.method == 'POST':
        formset = ServicioTecnicoContactoInlineFormset(request.POST, instance=service, prefix='st_dc')
        if formset.is_valid():
            formset.save()
            return redirect(to='index')
    else:
        formset = ServicioTecnicoContactoInlineFormset(instance=service, prefix='st_dc')
    return render(request, 'base_formset.html', context={'service': service,
                                                         'formset': formset,
                                                         'template_name': 'resumen/resumen_service.html',
                                                         'modelo': 'Servicio Técnico',
                                                         'titulo': 'Dato de Contacto',
                                                         'id': service.pk,
                                                         'nombre_vista': 'st_alta_dc'})


@login_required
@permission_required('gestion_imprenta.add_domicilio', raise_exception=True)
def service_alta_domicilio(request, id_service):
    service = ServicioTecnico.objects.get(pk=id_service)

    if request.method == 'POST':
        formset = ServicioTecnicoDomicilioInlineFormset(request.POST, instance=service, prefix='st_dc')
        if formset.is_valid():
            formset.save()
            return redirect(to='index')
    else:
        formset = ServicioTecnicoDomicilioInlineFormset(instance=service, prefix='st_dc')
    return render(request, 'base_formset.html', context={'service': service,
                                                         'formset': formset,
                                                         'template_name': 'resumen/resumen_service.html',
                                                         'modelo': 'Servicio Técnico',
                                                         'titulo': 'Domicilio',
                                                         'id': service.pk,
                                                         'nombre_vista': 'st_alta_domicilio'})


"""
    Trabajos
"""


@login_required
@permission_required('gestion_imprenta.add_trabajo', raise_exception=True)
def alta_trabajo(request):
    materiales_vigentes = Material.objects.filter(flg_activo=True)

    if request.method == 'POST':
        form = TrabajoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to='index')
    else:
        form = TrabajoForm()
        form.fields['materiales'].queryset = materiales_vigentes
    return render(request, 'base_alta_entidad.html', context={'form': form, 'modelo': 'Trabajo'})


@login_required
@permission_required('gestion_imprenta.add_cantidad', raise_exception=True)
def alta_cantidad(request):
    if request.method == 'POST':
        form = CantidadForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to='index')
    else:
        form = CantidadForm()
    return render(request, 'base_alta_entidad.html', context={'form': form, 'modelo': 'Cantidad'})


@login_required
@permission_required('gestion_imprenta.add_trabajocantidades', raise_exception=True)
def trabajo_cantidad(request, id_trabajo):
    cantidades_vigentes = Cantidad.objects.filter(flg_activo=True)

    trabajo = Trabajo.objects.get(pk=id_trabajo)

    if request.method == 'POST':
        formset = TrabajoCantidadInlineFormset(request.POST, instance=trabajo, prefix='tc')
        if formset.is_valid():
            formset.save()
            return redirect(to='index')
    else:
        formset = TrabajoCantidadInlineFormset(instance=trabajo, prefix='tc')
        for f in formset:
            f.fields['cantidad'].queryset = cantidades_vigentes
    return render(request, 'base_formset.html', context={'trabajo': trabajo,
                                                         'formset': formset,
                                                         'template_name': 'resumen/resumen_trabajo.html',
                                                         'modelo': 'Trabajo',
                                                         'titulo': 'Cantidades',
                                                         'id': trabajo.pk,
                                                         'nombre_vista': 'trabajo_cantidad'})


@login_required
@permission_required('gestion_imprenta.add_trabajoterminaciones', raise_exception=True)
def trabajo_terminacion(request, id_trabajo):
    terminaciones_vigentes = Terminacion.objects.filter(flg_activo=True)
    trabajo = Trabajo.objects.get(pk=id_trabajo)

    if request.method == 'POST':
        formset = TrabajoTerminacionInlineFormset(request.POST, instance=trabajo, prefix='tt')
        if formset.is_valid():
            formset.save()
            return redirect(to='index')
    else:
        formset = TrabajoTerminacionInlineFormset(instance=trabajo, prefix='tt')
        for f in formset.forms:
            f.fields['terminacion'].queryset = terminaciones_vigentes

    return render(request, 'base_formset.html', context={'trabajo': trabajo,
                                                         'formset': formset,
                                                         'template_name': 'resumen/resumen_trabajo.html',
                                                         'modelo': 'Trabajo',
                                                         'titulo': 'Terminaciones',
                                                         'id': trabajo.pk,
                                                         'nombre_vista': 'trabajo_terminacion'})


class ListaTrabajos(LoginRequiredMixin, ListView):
    queryset = Trabajo.objects.all()
    template_name = "listas/trabajo_lista.html"
    context_object_name = 'lista'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Trabajos'
        return context


class DetalleTrabajo(LoginRequiredMixin, DetailView):
    template_name = 'detalle/trabajo_detalle.html'
    queryset = Trabajo.objects.all()
    context_object_name = 'trabajo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = context.get('trabajo').trabajo_descripcion

        return context


@login_required
@permission_required('gestion_imprenta.add_medidaestandar', raise_exception=True)
def alta_medida_estandar(request):
    if request.method == 'POST':
        form = MedidaEstandarForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to='index')
    else:
        form = MedidaEstandarForm()
    return render(request, 'base_alta_entidad.html', context={'form': form, 'modelo': 'Medida'})


@login_required
@permission_required('gestion_imprenta.add_material', raise_exception=True)
def alta_material(request):
    proveedores_vigentes = Proveedor.objects.filter(flg_activo=True)

    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='index')
    else:
        form = MaterialForm()
        form.fields['material_proveedor'].queryset = proveedores_vigentes
    return render(request, 'base_alta_entidad.html', context={'form': form, 'modelo': 'Material'})


class ListaMateriales(LoginRequiredMixin, ListView):
    queryset = Material.objects.all()
    template_name = "listas/material_lista.html"
    context_object_name = 'lista'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Materiales'
        return context


class DetalleMaterial(LoginRequiredMixin, DetailView):
    template_name = 'detalle/material_detalle.html'
    queryset = Material.objects.all()
    context_object_name = 'material'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = context.get('material').material_descripcion
        return context


@login_required
@permission_required('gestion_imprenta.add_maquinapliego', raise_exception=True)
def alta_maq_pliego(request):
    sv_vigentes = ServicioTecnico.objects.filter(flg_activo=True)

    if request.method == 'POST':
        form = MaquinaPliegoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to='index')
    else:
        form = MaquinaPliegoForm()
        form.fields['servicio_tecnico'].queryset = sv_vigentes
    return render(request, 'base_alta_entidad.html', context={'form': form, 'modelo': 'Maquina Impresión'})


@login_required
@permission_required('gestion_imprenta.add_maquinapliegocolores', raise_exception=True)
def maq_pliego_color(request, id_maquina):
    colores_vigentes = ColorImpresion.objects.filter(flg_activo=True)
    maq_pliego = MaquinaPliego.objects.get(pk=id_maquina)

    if request.method == 'POST':
        formset = MaquinaPliegoColorInlineFormset(request.POST, instance=maq_pliego, prefix='mp')
        if formset.is_valid():
            formset.save()
            return redirect(to='index')
    else:
        formset = MaquinaPliegoColorInlineFormset(instance=maq_pliego, prefix='mp')
        for f in formset:
            f.fields['color_impresion'].queryset = colores_vigentes

    return render(request, 'base_formset.html', context={'maquina_pliego': maq_pliego,
                                                         'formset': formset,
                                                         'template_name': 'resumen/resumen_maquina_pliego.html',
                                                         'modelo': 'Maquina Impresión',
                                                         'titulo': 'Asignación Color',
                                                         'id': maq_pliego.pk,
                                                         'nombre_vista': 'maq_pliego_color'})


@login_required
@permission_required('gestion_imprenta.add_maquinaterminacion', raise_exception=True)
def alta_maq_terminacion(request):
    sv_vigentes = ServicioTecnico.objects.filter(flg_activo=True)
    if request.method == 'POST':
        form = MaquinaTerminacionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to='index')
    else:
        form = MaquinaTerminacionForm()
        form.fields['servicio_tecnico'].queryset = sv_vigentes
    return render(request, 'base_alta_entidad.html', context={'form': form, 'modelo': 'Maquina Terminación'})


@login_required
@permission_required('gestion_imprenta.add_envio', raise_exception=True)
def alta_envio(request):
    if request.method == 'POST':
        form = EnvioForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to='index')
    else:
        form = EnvioForm()
    return render(request, 'base_alta_entidad.html', context={'form': form, 'modelo': 'Envío'})


@login_required
@permission_required('gestion_imprenta.add_estado', raise_exception=True)
def alta_estado(request):
    if request.method == 'POST':
        form = EstadoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to='index')
    else:
        form = EstadoForm()
    return render(request, 'base_alta_entidad.html', context={'form': form, 'modelo': 'Estado'})


@login_required
@permission_required('gestion_imprenta.add_tipoterminacion', raise_exception=True)
def alta_tipo_terminacion(request):
    if request.method == 'POST':
        form = TipoTerminacionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to='index')
    else:
        form = TipoTerminacionForm()
    return render(request, 'base_alta_entidad.html', context={'form': form, 'modelo': 'Tipo de terminación'})


@login_required
@permission_required('gestion_imprenta.add_terminacion', raise_exception=True)
def alta_terminacion(request):
    tipo_terminacion_vigentes = TipoTerminacion.objects.filter(flg_activo=True)

    if request.method == 'POST':
        form = TerminacionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to='index')
    else:
        form = TerminacionForm()
        form.fields['tipo_terminacion'].queryset = tipo_terminacion_vigentes
    return render(request, 'base_alta_entidad.html', context={'form': form, 'modelo': 'Terminación'})


@login_required
@permission_required('gestion_imprenta.add_terminacionesmaquinas', raise_exception=True)
def terminacion_maquina(request, id_terminacion):
    terminacion = Terminacion.objects.get(pk=id_terminacion)
    maquinas_vigentes = MaquinaTerminacion.objects.filter(flg_activo=True)

    if request.method == 'POST':
        formset = TerminacionesMaquinasInlineFormset(request.POST, instance=terminacion, prefix='tm')
        if formset.is_valid():
            formset.save()
            return redirect(to='index')
    else:
        formset = TerminacionesMaquinasInlineFormset(instance=terminacion, prefix='tm')
        for f in formset:
            f.fields['maquina_terminacion'].queryset = maquinas_vigentes

    return render(request, 'base_formset.html', context={'terminacion': terminacion,
                                                         'formset': formset,
                                                         'template_name': 'resumen/resumen_terminacion.html',
                                                         'modelo': 'Terminación',
                                                         'titulo': 'Máquinas Terminación',
                                                         'id': terminacion.pk,
                                                         'nombre_vista': 'terminacion_maquina'})


def solicitud_terminaciones(request, id_solicitud):
    solicitud = SolicitudPresupuesto.objects.get(pk=id_solicitud)

    if request.method == 'POST':
        formset = TerminacionesSolicitudInlineFormset(request.POST, instance=solicitud, prefix='sol_term')
        if formset.is_valid():
            formset.save()
            return redirect(to='detalle_solicitud', pk=solicitud.pk)
    else:
        formset = TerminacionesSolicitudInlineFormset(instance=solicitud, prefix='sol_term')
        for f in formset:
            maquinas_vigentes = MaquinaTerminacion.objects.filter(flg_activo=True,
                                                                  terminacionesmaquinas__terminacion=f.instance.terminacion,
                                                                  terminacionesmaquinas__flg_activo=True)
            f.fields['maquina_terminacion'].queryset = maquinas_vigentes

    return render(request, 'edicion_formset.html', context={'solicitud': solicitud,
                                                            'formset': formset,
                                                            'titulo': 'Terminaciones de la Solicitud',
                                                            'id': solicitud.pk,
                                                            'nombre_vista': 'solicitud_terminaciones'})


@login_required
@permission_required(perm=['gestion_imprenta.add_comentario'], raise_exception=True)
def solicitud_comentarios(request, id_solicitud):
    solicitud = SolicitudPresupuesto.objects.get(pk=id_solicitud)

    if request.method == 'POST':
        form = ComentariosForm(request.POST, prefix='sol_com')

        if form.is_valid():
            comentario = form.save(commit=False)
            if comentario.usuario is None:
                comentario.usuario = request.user
                comentario.solicitud = solicitud
            form.save()
        return redirect(to='detalle_solicitud', pk=solicitud.pk)
    else:
        form = ComentariosForm(prefix='sol_com')

    return render(request, 'base_alta_entidad.html', context={'form': form,
                                                              'modelo': 'Comentarios'})


class ListaSolicitudes(LoginRequiredMixin, ListView):
    queryset = SolicitudPresupuesto.objects.exclude(
        presupuesto__presupuestoestado__estado__estado_descripcion='Aceptado por el cliente'
    ).order_by('-solicitud_express_flg', 'solicitud_fecha')
    template_name = "listas/solicitudes_lista.html"
    context_object_name = 'lista'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Solicitudes'
        return context


class DetalleSolicitudes(LoginRequiredMixin, DetailView):
    template_name = 'detalle/solicitudes_detalle.html'
    queryset = SolicitudPresupuesto.objects.all()
    context_object_name = 'solicitud'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cantidad_hojas'] = context.get('solicitud').cantidad_hojas_impresion()
        costo_impresion, costo_material, costo_terminacion = context.get('solicitud').calculo_presupuesto()

        context['costo_impresion'] = costo_impresion
        context['costo_material'] = costo_material
        context['costo_terminaciones'] = costo_terminacion
        context['costo_total_s_disenio'] = costo_impresion + costo_material + costo_terminacion

        return context


@login_required
@permission_required(perm=['gestion_imprenta.cambiar_maquina_pliego'], raise_exception=True)
def solicitud_maquina_impresion(request, id_solicitud):
    solicitud = SolicitudPresupuesto.objects.get(pk=id_solicitud)
    maquinas_impresion = MaquinaPliego.objects.filter(flg_activo=True,
                                                      maquinapliegocolores__color_impresion=solicitud.color_impresion,
                                                      maquinapliegocolores__flg_activo=True)
    if request.method == 'POST':
        form = SolicitudPresupuestoForm(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()
            return redirect(to='detalle_solicitud', pk=solicitud.pk)
    else:
        form = SolicitudPresupuestoForm(instance=solicitud)
        form.fields['maquina_pliego'].queryset = maquinas_impresion

    return render(request, 'base_alta_entidad.html', context={'solicitud': solicitud,
                                                              'titulo': 'Asignación máquina para imprimir',
                                                              'id': solicitud.pk,
                                                              'nombre_vista': 'solicitud_impresion',
                                                              'form': form, 'modelo': 'Solicitud Impresión'})


@login_required
@permission_required(perm=['gestion_imprenta.generar_presupuesto'], raise_exception=True)
def solicitud_presupuesto(request, id_solicitud):
    decimales = Decimal(10) ** -3

    solicitud = SolicitudPresupuesto.objects.get(pk=id_solicitud)
    cant_hojas = solicitud.cantidad_hojas_impresion()
    costo_impresion, costo_material, costo_terminacion = solicitud.calculo_presupuesto()

    if request.method == 'POST':
        form = PresupuestoForm(request.POST)

        if form.is_valid():
            presupuesto = form.save(commit=False)
            presupuesto.solicitud = solicitud
            presupuesto.hojas_utilizadas = cant_hojas
            presupuesto.costo_impresion_dolar = costo_impresion
            presupuesto.costo_material_dolar = costo_material
            presupuesto.costo_terminaciones_dolar = costo_terminacion

            if presupuesto.costo_disenio is not None:
                costo_total_dolar = costo_material + costo_impresion + costo_terminacion + (
                            presupuesto.costo_disenio / presupuesto.cotizacion_dolar)
            else:
                costo_total_dolar = costo_material + costo_impresion + costo_terminacion
                presupuesto.costo_disenio = 0

            presupuesto.costo_total_dolar = costo_total_dolar
            presupuesto.costo_unitario_dolar = costo_total_dolar / solicitud.cantidad_estandar.cantidad

            costo_total_pesificado = (costo_total_dolar * presupuesto.cotizacion_dolar)
            costo_total_pesificado.quantize(decimales)

            presupuesto.precio_cliente = costo_total_pesificado / (1 - (presupuesto.margen_ganancia / 100))
            form.save()
            estado_creado = Estado.objects.get(tipo_estado='Inicial', flg_activo=True, entidad_asociada='presupuesto')
            presupuesto.presupuestoestado_set.create(estado=estado_creado, fecha_cambio_estado=datetime.now(),
                                                     usuario=request.user)

            return redirect(to='detalle_solicitud', pk=solicitud.pk)
    else:
        form = PresupuestoForm()

    return render(request, 'presupuesto_alta.html', context={'form': form,
                                                             'disenio_incluido': solicitud.solicitud_disenio_flg,
                                                              'modelo': "Presupuesto"})


@login_required
@permission_required(perm=['gestion_imprenta.add_solicitudpresupuestocontactos'], raise_exception=True)
def solicitud_contacto(request,id_solicitud):
    solicitud = SolicitudPresupuesto.objects.get(pk=id_solicitud)

    if request.method == 'POST':
        form_cliente = ClienteForm(request.POST, prefix='cliente')
        form_contacto = DatoContactoForm(request.POST, prefix='contacto')
        form_cliente.fields['cliente_origen'].choices = [('manual', 'Manual')]
        form_solicitud_contacto = SolicitudPresupuestoContactoForm(request.POST, prefix='sol_contacto')

        if form_cliente.is_valid() and form_contacto.is_valid() and form_solicitud_contacto.is_valid():
            cliente = form_cliente.save()

            contacto = form_contacto.save(commit=False)
            contacto.cliente = cliente
            contacto.save()

            sol_pre_contacto = form_solicitud_contacto.save(commit=False)
            sol_pre_contacto.contacto = contacto
            sol_pre_contacto.solicitud = solicitud
            sol_pre_contacto.fecha_creacion = datetime.now()
            sol_pre_contacto.save()

            return redirect(to='detalle_solicitud', pk=solicitud.pk)

    else:
        form_cliente = ClienteForm(prefix='cliente')
        form_contacto = DatoContactoForm(prefix='contacto')
        form_cliente.fields['cliente_origen'].choices = [('manual', 'Manual')]
        form_solicitud_contacto = SolicitudPresupuestoContactoForm(prefix='sol_contacto')

    return render(request, 'forms_juntos.html', context={'form_1': form_cliente,
                                                         'form_2': form_contacto,
                                                         'form_3': form_solicitud_contacto,
                                                         'solicitud':solicitud,
                                                         'url_action':'solicitud_contacto',
                                                         'clave': solicitud.pk})


@login_required
@permission_required(perm=['gestion_imprenta.change_solicitudpresupuestocontactos'], raise_exception=True)
def solicitud_contacto_edicion(request, id_solicitud_contacto):
    solicitud_contacto = SolicitudPresupuestoContactos.objects.get(pk=id_solicitud_contacto)

    if request.method == 'POST':
        form_cliente = ClienteForm(request.POST, prefix='cliente', instance=solicitud_contacto.contacto.cliente)
        form_contacto = DatoContactoForm(request.POST, prefix='contacto', instance=solicitud_contacto.contacto)
        form_cliente.fields['cliente_origen'].choices = [('manual', 'Manual')]
        form_solicitud_contacto = SolicitudPresupuestoContactoForm(request.POST, prefix='sol_contacto',
                                                                   instance=solicitud_contacto)

        if form_cliente.is_valid() and form_contacto.is_valid() and form_solicitud_contacto.is_valid():
            form_cliente.save()
            form_contacto.save()
            form_solicitud_contacto.save()

            return redirect(to='detalle_solicitud', pk=solicitud_contacto.solicitud.pk)

    else:
        form_cliente = ClienteForm(prefix='cliente', instance=solicitud_contacto.contacto.cliente)
        form_contacto = DatoContactoForm(prefix='contacto', instance=solicitud_contacto.contacto)
        form_cliente.fields['cliente_origen'].choices = [('manual', 'Manual')]
        form_solicitud_contacto = SolicitudPresupuestoContactoForm(prefix='sol_contacto', instance=solicitud_contacto)

    return render(request, 'forms_juntos.html', context={'form_1': form_cliente,
                                                         'form_2': form_contacto,
                                                         'form_3': form_solicitud_contacto,
                                                         'solicitud':solicitud_contacto.solicitud,
                                                         'url_action': 'editar_solicitud_contacto',
                                                         'clave': solicitud_contacto.pk})


@login_required
@permission_required(perm=['gestion_imprenta.delete_solicitudpresupuestocontactos'], raise_exception=True)
def solcitud_contacto_eliminar(request, id_contacto):
    solicitud_contacto = SolicitudPresupuestoContactos.objects.get(pk=id_contacto)
    solicitud = SolicitudPresupuesto.objects.get(pk=solicitud_contacto.solicitud.pk)
    solicitud_contacto.delete()
    messages.success(request, ('Task has been Deleted!'))
    return redirect(to='detalle_solicitud', pk=solicitud.pk)


class ListaPresupuestos(LoginRequiredMixin, ListView):
    queryset = Presupuesto.objects.filter(ordentrabajo__presupuesto__isnull=True)
    template_name = "listas/presupuesto_lista.html"
    permission_required('gestion_imprenta.add_presupuesto')
    context_object_name = 'lista'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Presupuestos'
        return context


class DetallePresupuesto(LoginRequiredMixin, DetailView):
    template_name = 'detalle/presupuesto_detalle.html'
    queryset = Presupuesto.objects.all()
    context_object_name = 'presupuesto'


@login_required
@permission_required(perm=['gestion_imprenta.add_comentario'], raise_exception=True)
def presupuesto_comentarios(request, id_presupuesto):
    presupuesto = Presupuesto.objects.get(pk=id_presupuesto)

    if request.method == 'POST':
        form = ComentariosForm(request.POST, prefix='pre_com')

        if form.is_valid():
            comentario = form.save(commit=False)
            if comentario.usuario is None:
                comentario.usuario = request.user
                comentario.presupuesto = presupuesto
            form.save()
        return redirect(to='detalle_presupuesto', pk=presupuesto.pk)
    else:
        form = ComentariosForm(prefix='pre_com')

    return render(request, 'base_alta_entidad.html', context={'form': form,
                                                              'modelo': 'Comentarios'})


@login_required
@permission_required(perm=['gestion_imprenta.add_presupuestoestado'], raise_exception=True)
def presupuesto_estado(request, id_presupuesto):
    presupuesto = Presupuesto.objects.get(pk=id_presupuesto)
    ultimo_estado = presupuesto.ultimo_estado().estado
    estados_posibles = Estado.objects.filter(entidad_asociada='presupuesto',flg_activo=True,
                                             estado_secuencia__gt=ultimo_estado.estado_secuencia)

    if request.method == 'POST':
        form = PresupuestoEstadoForm(request.POST, prefix='pre_est')

        if form.is_valid():
            nuevo_estado = form.save(commit=False)
            if nuevo_estado.usuario is None:
                nuevo_estado.usuario = request.user
                nuevo_estado.presupuesto = presupuesto
                nuevo_estado.fecha_cambio_estado = datetime.now()
            form.save()
        return redirect(to='detalle_presupuesto', pk=presupuesto.pk)
    else:
        form = PresupuestoEstadoForm(prefix='pre_est')
        form.fields.get('estado').queryset = estados_posibles
    return render(request, 'base_alta_entidad.html', context={'form': form,
                                                              'modelo': 'Nuevo estado'})


@login_required
@permission_required(perm=['gestion_imprenta.add_ordentrabajo'], raise_exception=True)
def presupuesto_orden_trabajo(request, id_presupuesto):
    """
    Esta función crea una nueva orden de trabajo a partir de un presupuesto
    :param request:
    :param id_presupuesto: id del presupuesto
    :return: una orden de trabajo
    """

    presupuesto = Presupuesto.objects.get(pk=id_presupuesto)
    orden_trabajo = OrdenTrabajo(presupuesto=presupuesto,
                                 orden_fecha_creacion=datetime.now(),
                                 orden_impresion_realizada_flg=False,
                                 orden_terminacion_realizada_flg=False,
                                 orden_disenio_realizado_flg=False)
    orden_trabajo.save()

    if presupuesto.solicitud.solicitud_disenio_flg:
        tarea_disenio = Tarea(tarea='disenio',
                              orden_trabajo=orden_trabajo,
                              fecha_creacion=datetime.now())
        tarea_disenio.save()
        tarea_historial = TareaHistorial(tarea=tarea_disenio,
                                         usuario=request.user,
                                         flg_realizado=False,
                                         fecha_registro=datetime.now())
        tarea_historial.save()

    if presupuesto.solicitud.solicitud_terminacion_flg:
        tarea_terminaciones = Tarea(tarea='terminaciones',
                                    orden_trabajo=orden_trabajo,
                                    fecha_creacion=datetime.now())
        tarea_disenio.save()
        tarea_historial = TareaHistorial(tarea=tarea_terminaciones,
                                         usuario=request.user,
                                         flg_realizado=False,
                                         fecha_registro=datetime.now())
        tarea_historial.save()

    tarea_impresion = Tarea(tarea='impresion',
                            orden_trabajo=orden_trabajo,
                            fecha_creacion=datetime.now())
    tarea_impresion.save()
    tarea_historial = TareaHistorial(tarea=tarea_impresion,
                                     usuario=request.user,
                                     flg_realizado=False,
                                     fecha_registro=datetime.now())
    tarea_historial.save()

    estado_inicial = Estado.objects.get(entidad_asociada='orden_trabajo', flg_activo=True, tipo_estado='Inicial')

    orden_trabajo_estado = OrdenTrabajoEstado(fecha_cambio_estado=datetime.now(),
                                              estado=estado_inicial,
                                              orden_trabajo=orden_trabajo,
                                              usuario=request.user)
    orden_trabajo_estado.save()

    return redirect(to='index')


class ListaOrdenesTrabajo(LoginRequiredMixin, ListView):
    queryset = OrdenTrabajo.objects.all()
    template_name = "listas/ordenes_trabajo_lista.html"
    context_object_name = 'lista'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Órdenes de trabajo'
        return context


class DetalleOrdenTrabajo(LoginRequiredMixin, DetailView):
    template_name = 'detalle/orden_trabajo_detalle.html'
    queryset = OrdenTrabajo.objects.all()
    context_object_name = 'ordentrabajo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Orden de trabajo - Nro: {}".format(context.get('ordentrabajo').pk)

        return context


@login_required
@permission_required(perm=['gestion_imprenta.add_ordentrabajoestado'], raise_exception=True)
def orden_trabajo_estado(request, orden_id):
    orden_trabajo = OrdenTrabajo.objects.get(pk=orden_id)
    ultimo_estado = orden_trabajo.ultimo_estado().estado
    estados_posibles = Estado.objects.filter(entidad_asociada='orden_trabajo',flg_activo=True,
                                             estado_secuencia__gt=ultimo_estado.estado_secuencia)

    if request.method == 'POST':
        form = OrdenTrabajoEstadoForm(request.POST, prefix='ot_est')

        if form.is_valid():
            nuevo_estado = form.save(commit=False)
            if nuevo_estado.usuario is None:
                nuevo_estado.usuario = request.user
                nuevo_estado.orden_trabajo = orden_trabajo
                nuevo_estado.fecha_cambio_estado = datetime.now()
            form.save()
        return redirect(to='detalle_orden_trabajo', pk=orden_trabajo.pk)
    else:
        form = OrdenTrabajoEstadoForm(prefix='ot_est')
        form.fields.get('estado').queryset = estados_posibles
    return render(request, 'base_alta_entidad.html', context={'form': form,
                                                              'modelo': 'Nuevo estado'})


def orden_trabajo_comentarios(request, orden_id):
    ot = OrdenTrabajo.objects.get(pk=orden_id)

    if request.method == 'POST':
        form = ComentariosForm(request.POST, prefix='ot_com')

        if form.is_valid():
            comentario = form.save(commit=False)
            if comentario.usuario is None:
                comentario.usuario = request.user
                comentario.orden = ot
            form.save()
        return redirect(to='detalle_orden_trabajo', pk=ot.pk)
    else:
        form = ComentariosForm(prefix='ot_com')

    return render(request, 'base_alta_entidad.html', context={'form': form,
                                                              'modelo': 'Comentarios'})


@login_required
@permission_required(perm=['gestion_imprenta.add_tarea'], raise_exception=True)
def crear_tarea(request, orden_id):
    orden_trabajo = OrdenTrabajo.objects.get(pk=orden_id)

    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.orden_trabajo = orden_trabajo
            tarea.usuario = request.user
            tarea.save()
            return redirect(to='detalle_orden_trabajo', pk=orden_trabajo.pk)
    else:
        form = TareaForm()

    return render(request, 'base_alta_entidad.html', context={'orden_trabajo': orden_trabajo,
                                                              'titulo': 'Nueva tarea',
                                                              'id': orden_trabajo.pk,
                                                              'nombre_vista': 'orden_trabajo_tarea',
                                                              'form': form, 'modelo': 'Tarea'})


@login_required
@permission_required(perm=['gestion_imprenta.change_tarea'], raise_exception=True)
def marcar_tarea(request, tarea_id):
    tarea = Tarea.objects.get(pk=tarea_id)
    historia = TareaHistorial(tarea=tarea, usuario=request.user, campo_actualizado="completa",
                              valor_anterior=False, valor_actualizado=True)
    tarea.completa = True
    tarea.save()
    historia.save()
    return redirect(to='detalle_orden_trabajo', pk=tarea.orden_trabajo.pk)


@login_required
@permission_required(perm=['gestion_imprenta.change_tarea'], raise_exception=True)
def desmarcar_tarea(request, tarea_id):
    tarea = Tarea.objects.get(pk=tarea_id)
    historia = TareaHistorial(tarea=tarea, usuario=request.user, campo_actualizado="completa",
                              valor_anterior=True, valor_actualizado=False)
    tarea.completa = False
    tarea.save()
    historia.save()
    return redirect(to='detalle_orden_trabajo', pk=tarea.orden_trabajo.pk)


@login_required
@permission_required(perm=['gestion_imprenta.delete_tarea', 'gestion_imprenta.delete_tareahistorial'], raise_exception=True)
def eliminar_tarea(request, tarea_id):
    tarea = Tarea.objects.get(pk=tarea_id)
    historial = TareaHistorial.objects.filter(tarea=tarea)
    historial.delete()
    tarea.delete()
    return redirect(to='detalle_orden_trabajo', pk=tarea.orden_trabajo.pk)


@login_required
@permission_required(perm=['gestion_imprenta.change_tarea'], raise_exception=True)
def editar_tarea(request, tarea_id):
    tarea =  Tarea.objects.get(pk=tarea_id)

    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            tarea = form.save(commit=False)

            for campo_editado in form.changed_data:
                historial = TareaHistorial(tarea=tarea, usuario=request.user, campo_actualizado=campo_editado,
                                           valor_anterior=form.initial.get(campo_editado),
                                           valor_actualizado=form.cleaned_data.get(campo_editado))
                historial.save()
            tarea.save()
            return redirect(to='detalle_orden_trabajo', pk=tarea.orden_trabajo.pk)
    else:
        form = TareaForm(instance=tarea)

    return render(request, 'base_alta_entidad.html', context={'tarea': tarea,
                                                              'titulo': 'Nueva tarea',
                                                              'id': tarea.pk,
                                                              'nombre_vista': 'editar_tarea',
                                                              'form': form, 'modelo': 'Tarea'})

