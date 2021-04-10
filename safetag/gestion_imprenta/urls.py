from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),

    path('cliente', views.alta_cliente, name='alta_cliente'),
    path('cliente/<int:id_cliente>/dato_contacto', views.cliente_alta_dato_contacto, name='cliente_alta_dc'),
    path('cliente/<int:id_cliente>/domicilio', views.cliente_alta_domicilio, name='cliente_alta_domicilio'),
    path('clientes', views.ListaClientes.as_view(), name='clientes'),
    path('cliente/<slug:pk>', views.DetalleCliente.as_view(), name='detalle_cliente'),

    path('proveedor', views.alta_proveedor, name='alta_proveedor'),
    path('proveedor/<int:id_proveedor>/dato_contacto', views.proveedor_alta_dato_contacto,
         name='proveedor_alta_dc'),
    path('proveedor/<int:id_proveedor>/domicilio', views.proveedor_alta_domicilio,
         name='proveedor_alta_domicilio'),

    path('servicio_tecnico', views.alta_servicio_tecnico, name='alta_servicio_tecnico'),
    path('servicio_tecnico/<int:id_service>/dato_contacto', views.service_alta_dato_contacto, name='st_alta_dc'),
    path('servicio_tecnico/<int:id_service>/domicilio', views.service_alta_domicilio, name='st_alta_domicilio'),

    path('trabajo', views.alta_trabajo, name='alta_trabajo'),
    path('trabajo/<int:id_trabajo>/cantidad', views.trabajo_cantidad, name='trabajo_cantidad'),
    path('trabajo/<int:id_trabajo>/terminacion', views.trabajo_terminacion, name='trabajo_terminacion'),
    path('trabajos', views.ListaTrabajos.as_view(), name='trabajos'),
    path('trabajo/<slug:pk>', views.DetalleTrabajo.as_view(), name='detalle_trabajo'),

    path('cantidad', views.alta_cantidad, name='alta_cantidad'),

    path('medida', views.alta_medida_estandar, name='alta_medida_estandar'),

    path('material', views.alta_material, name='alta_material'),

    path('maquina_impresion', views.alta_maq_pliego, name='alta_maq_pliego'),
    path('maquina_impresion/<int:id_maquina>/color', views.maq_pliego_color, name='maq_pliego_color'),

    path('terminacion', views.alta_terminacion, name='alta_terminacion'),
    path('terminacion/<int:id_terminacion>/maquina', views.terminacion_maquina, name='terminacion_maquina'),
    path('tipo_terminacion', views.alta_tipo_terminacion, name='alta_tipo_terminacion'),

    path('maquina_terminacion', views.alta_maq_terminacion, name='alta_maq_terminacion'),

    path('envio', views.alta_envio, name='alta_envio'),

    path('estado', views.alta_estado, name='alta_estado'),
    path('subestado', views.alta_subestado, name='alta_estado'),

    path('solicitudes', views.ListaSolicitudes.as_view(), name='solicitudes'),
    path('solicitud/<slug:pk>/', views.DetalleSolicitudes.as_view(), name='detalle_solicitud'),
    path('solicitud/<int:id_solicitud>/terminaciones', views.solicitud_terminaciones, name='solicitud_terminaciones'),
    path('solicitud/<int:id_solicitud>/comentarios', views.solicitud_comentarios, name='solicitud_comentarios'),
    path('solicitud/<int:id_solicitud>/impresion', views.solicitud_maquina_impresion, name='solicitud_impresion'),
    path('solicitud/<int:id_solicitud>/presupuesto', views.solicitud_presupuesto, name='solicitud_presupuesto'),

    path('presupuestos', views.ListaPresupuestos.as_view(), name='presupuestos'),
    path('presupuesto/<slug:pk>/', views.DetallePresupuesto.as_view(), name='detalle_presupuesto'),
    path('presupuesto/<int:id_presupuesto>/comentarios', views.presupuesto_comentarios, name='presupuesto_comentarios'),
    path('presupuesto/<int:id_presupuesto>/estado', views.presupuesto_estado, name='presupuesto_estado'),
    path('presupuesto/<int:id_presupuesto>/orden_trabajo', views.presupuesto_orden_trabajo,
         name='presupuesto_orden_trabajo'),

    path('ordenes_trabajo', views.ListaOrdenesTrabajo.as_view(), name='ordenes_trabajo'),
    path('orden_trabajo/<slug:pk>/', views.DetalleOrdenTrabajo.as_view(), name='detalle_orden_trabajo'),
    path('orden_trabajo/<int:orden_id>/estado', views.orden_trabajo_estado, name='orden_trabajo_estado'),
    path('orden_trabajo/<int:orden_id>/subestado', views.orden_trabajo_subsestado, name='orden_trabajo_subestado'),
    path('orden_trabajo/<int:orden_id>/comentarios', views.orden_trabajo_comentarios, name='orden_trabajo_comentarios'),

    path('login/', auth_views.LoginView.as_view(template_name='cuentas/usuario_login.html',
                                                redirect_field_name='next',
                                                extra_context={'url': 'index'}), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='cuentas/usuario_logout.html'), name='logout'),
    path('password_reset/', auth_views.PasswordChangeView.as_view(template_name='cuentas/usuario_reset_pass.html'),
         name='password_reset')
]
